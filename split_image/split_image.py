import argparse
import os, sys
from PIL import Image
from datetime import datetime
from tqdm import tqdm

# avoid DOS bomb warning
Image.MAX_IMAGE_PIXELS = 1000000000

def split_image(img, target_w, target_h):
  orig_w, orig_h = img.size
  index = 0

  for h1 in range(int(orig_h / target_h)):
    for w1 in range(int(orig_w / target_w)):
      w2 = w1 * target_w
      h2 = h1 * target_h
      yield (index, img.crop((w2, h2, (w2 + target_w) , (h2 + target_h))))
      index += 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--src_dir', type=str, help='directory for image files')
  parser.add_argument('--dst_dir', type=str, help='Output directory')
  parser.add_argument('--size', type=int, default='257', help='target image size(square)')
  args = parser.parse_args()

  for f in tqdm(os.listdir(args.src_dir)):
    base, ext = os.path.splitext(os.path.basename(f))
    im = Image.open(os.path.join(args.src_dir, f))
    for index, out in split_image(im, args.size, args.size):
      out.save(os.path.join(args.dst_dir, base+'_'+str(index)+ext))
