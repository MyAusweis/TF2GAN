# -*- coding: utf-8 -*-

import os, argparse
from dataloader import Dataloader
from model import Model
import sys
sys.path.append('..')
from utils import check_dir

def parse_args():
	desc = 'TensorFlow 2.0 implementation of UNet'
	parser = argparse.ArgumentParser(description=desc)

	parser.add_argument('--dataset_name', type=str, default='CelebAMask19')
	parser.add_argument('--phase', type=str, default='tfrecord', choices=('tfrecord', 'train', 'test'))
	parser.add_argument('--img_size', type=int, default=256)
	parser.add_argument('--img_nc', type=int, default=3)
	parser.add_argument('--batch_size', type=int, default=16)

	parser.add_argument('--epochs', type=int, default=15)
	parser.add_argument('--decay_epochs', type=int, default=15)
	parser.add_argument('--lr', type=float, default=0.0002)
	
	parser.add_argument('--log_freq', type=int, default=1000)
	parser.add_argument('--output_dir', type=str, default='output')
	parser.add_argument('--log_dir', type=str, default='log')
	parser.add_argument('--sample_dir', type=str, default='sample')
	parser.add_argument('--save_dir', type=str, default='model')
	parser.add_argument('--result_dir', type=str, default='result')

	parser.add_argument('--test_img_dir', type=str, default='img')

	args = parser.parse_args()
	check_dir(args.output_dir)
	args.output_dir = os.path.join(args.output_dir, f'UNet_{args.dataset_name}')
	check_dir(args.output_dir)
	args.log_dir = os.path.join(args.output_dir, args.log_dir)
	check_dir(args.log_dir)
	args.sample_dir = os.path.join(args.output_dir, args.sample_dir)
	check_dir(args.sample_dir)
	args.save_dir = os.path.join(args.output_dir, args.save_dir)
	check_dir(args.save_dir)
	args.result_dir = os.path.join(args.output_dir, args.result_dir)
	check_dir(args.result_dir)

	if args.dataset_name == 'CelebAMask19':
		args.label_names = ['background', 'skin', 'nose', 'eye_g', 'l_eye', 'r_eye', 'l_brow', 'r_brow', 
			'l_ear', 'r_ear', 'mouth', 'u_lip', 'l_lip', 'hair', 'hat', 'ear_r', 'neck_l', 'neck', 'cloth']
		args.label_nc = len(args.label_names)

	return args

if __name__ == '__main__':
	args = parse_args()
	if args.phase == 'tfrecord':
		print('Converting data to tfrecord...')
		Dataloader(args)
		print('Convert finished...')

	else:
		model = Model(args)
		model.build_model()

		if args.phase == 'train':
			print('Training...')
			model.train()
			print('Train finished...')
		
		elif args.phase == 'test':
			print('Testing...')
			model.test()
			print('Test finished...')