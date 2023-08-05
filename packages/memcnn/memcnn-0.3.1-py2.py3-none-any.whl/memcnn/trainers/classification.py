import os
import time
import logging
import torch
from memcnn.utils.stats import AverageMeter, accuracy
from memcnn.utils.tensorboard import parse_logs
from tensorboardX import SummaryWriter


logger = logging.getLogger('trainer')


def validate(model, ceriterion, val_loader, device):
    """validation sub-loop"""
    model.eval()

    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    end = time.time()
    with torch.no_grad():
        for ind, (x, label) in enumerate(val_loader):
            x, label = x.to(device), label.to(device)
            vx, vl = x, label

            score = model(vx)
            loss = ceriterion(score, vl)
            prec1 = accuracy(score.data, label)

            losses.update(loss.item(), x.size(0))
            top1.update(prec1[0][0], x.size(0))

            batch_time.update(time.time() - end)
            end = time.time()

    logger.info('Test: [{0}/{0}]\t'
                'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                'Prec@1 {top1.val:.3f} ({top1.avg:.3f})\t'.format(len(val_loader),
                                                                  batch_time=batch_time, loss=losses, top1=top1))

    return top1.avg, losses.avg


def train(manager,
          train_loader,
          test_loader,
          start_iter,
          disp_iter=100,
          save_iter=10000,
          valid_iter=1000,
          use_cuda=False,
          loss=None):
    """train loop"""

    device = 'cpu' if not use_cuda else 'cuda'
    model, optimizer = manager.model, manager.optimizer

    writer = SummaryWriter(manager.log_dir)
    data_time = AverageMeter()
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    ceriterion = loss
    # ensure train_loader enumerates to max_epoch
    max_iterations = train_loader.sampler.nsamples // train_loader.batch_size
    train_loader.sampler.nsamples = train_loader.sampler.nsamples - start_iter
    end = time.time()
    for ind, (x, label) in enumerate(train_loader):
        iteration = ind + 1 + start_iter

        if iteration > max_iterations:
            logger.info('maximum number of iterations reached: {}/{}'.format(iteration, max_iterations))
            break

        if iteration == 40000 or iteration == 60000:
            for param_group in optimizer.param_groups:
                param_group['lr'] *= 0.1

        model.train()

        data_time.update(time.time() - end)
        end = time.time()
        x, label = x.to(device), label.to(device)
        vx, vl = x, label

        score = model(vx)
        loss = ceriterion(score, vl)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        batch_time.update(time.time()-end)
        prec1 = accuracy(score.data, label)

        losses.update(loss.item(), x.size(0))
        top1.update(prec1[0][0], x.size(0))

        if iteration % disp_iter == 0:
            logger.info('iteration: [{0}/{1}]\t'
                        'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                        'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
                        'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                        'Prec@1 {top1.val:.3f} ({top1.avg:.3f})\t'.format(iteration, max_iterations,
                                                                          batch_time=batch_time, data_time=data_time,
                                                                          loss=losses, top1=top1))

        if iteration % disp_iter == 0:
            writer.add_scalar('train_loss', loss.item(), iteration)
            writer.add_scalar('train_acc', prec1[0][0], iteration)
            losses.reset()
            top1.reset()
            data_time.reset()
            batch_time.reset()

        if iteration % valid_iter == 0:
            test_top1, test_loss = validate(model, ceriterion, test_loader, device=device)
            writer.add_scalar('test_loss', test_loss, iteration)
            writer.add_scalar('test_acc', test_top1, iteration)

        if iteration % save_iter == 0:
            manager.save_train_state(iteration)

        end = time.time()

    writer.close()

    # Generate final scalars.json summary file from all generated log_files
    parse_logs(manager.log_dir, os.path.join(manager.log_dir, "scalars.json"))
