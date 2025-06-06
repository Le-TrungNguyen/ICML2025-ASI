# Measure on 1 batch of Cityscapes
SVD_var="0.4 0.5 0.6 0.7 0.8 0.9"
echo "Running with SVD_var=$SVD_var"
python train.py configs/fcn/hosvd_10L_fcn_r18-d8_512x512_cityscapes.py \
    --load-from calib/calib_fcn_r18-d8_512x512_1k_voc12aug_cityscapes/version_0/latest.pth \
    --cfg-options data.samples_per_gpu=8 \
    --seed 233 \
    --measure_perplexity True \
    --SVD_var "$SVD_var"