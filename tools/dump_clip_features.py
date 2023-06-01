import argparse
import clip
import csv
import json
import torch
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_path', default='/data/pcl/object-centric-ovd/datasets/zeroshot_weights/DIOR_rs_clip_a+photo+cname.npy')
    parser.add_argument('--prompt', default='photo')
    parser.add_argument('--model', default='clip')
    parser.add_argument('--clip_model', default="ViT-B/32")
    args = parser.parse_args()

    cat_names = []
    with open('tools/category_id_info.csv', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            label, value = row
            value = int(value)
            cat_names.append(label)

    print('cat_names', cat_names)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using prompt, ", args.prompt)

    sentences = ['a photo of a {}'.format(x) for x in cat_names]

    print('Loading CLIP')
    model, preprocess = clip.load(args.clip_model, device=device)
    text = clip.tokenize(sentences).to(device)
    with torch.no_grad():
        if len(text) > 10000:
            text_features = torch.cat([
                model.encode_text(text[:len(text) // 2]),
                model.encode_text(text[len(text) // 2:])],
                dim=0)
        else:
            text_features = model.encode_text(text)
    print('text_features.shape', text_features.shape)
    text_features = text_features.cpu().numpy()
    if args.out_path != '':
        print('saveing to', args.out_path)
        np.save(open(args.out_path, 'wb'), text_features)
