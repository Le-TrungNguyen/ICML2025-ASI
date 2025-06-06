# Measure on 1 batch of Cityscapes
SVD_var="0.4 0.5 0.6 0.7 0.8 0.9"
echo "Running with SVD_var=$SVD_var"
python train.py configs/upernet/hosvd_10L_upernet_r18_512x512_20k_cityscapes.py \
    --load-from calib/calib_upernet_r18_512x512_1k_voc12aug_cityscapes/version_0/latest.pth \
    --cfg-options data.samples_per_gpu=8 \
    --seed 233 \
    --measure_perplexity True \
    --SVD_var "$SVD_var"