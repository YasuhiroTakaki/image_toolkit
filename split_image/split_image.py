import argparse
import os, sys
from PIL import Image

from datetime import datetime

def split_image(img, target_w, target_h):
  orig_w, orig_h = img.size
  index = 0

  # 縦の分割枚数
  for h1 in range(int(orig_w / target_w)):
    # 横の分割枚数
    for w1 in range(int(orig_h / target_h)):
      w2 = w1 * target_w
      h2 = h1 * target_h
      print(w2, h2, target_w + w2, target_h + h2)
      yield (index, img.crop((w2, h2, target_w + w2, target_h + h2)))
      index += 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--src_dir', type=str, help='directory for image files')
  parser.add_argument('--dst_dir', type=str, help='Output directory')
  parser.add_argument('--size', type=int, default='257', help='target image size(square)')
  args = parser.parse_args()

  # 画像の読み込み
  for f in os.listdir(args.src_dir):
    base, ext = os.path.splitext(os.path.basename(f))
    im = Image.open(os.path.join(args.src_dir, f))
    for index, ig in split_image(im, 257, 257):
      # 保存先フォルダの指定
      ig.save(os.path.join(args.dst_dir, base+'_'+str(index)+ext))
