python train.py configs/deeplabv3mv2/0.8/hosvd_5L_deeplabv3_mv2_512x512_20k_voc12aug.py \
    --load-from calib/calib_deeplabv3_mv2_512x512_5k_voc12aug_cityscapes/version_0/latest.pth \
    --cfg-options data.samples_per_gpu=8 \
    --seed 233 \
    --with_ASI True \
    --perplexity_pkl "perplexity/perplexity_hosvd_10L_deeplabv3_mv2_512x512_20k_cityscapes/perplexity_combined.pkl"\
    --budget 0.626441180706024

python train.py configs/deeplabv3mv2/0.8/hosvd_10L_deeplabv3_mv2_512x512_20k_voc12aug.py \
    --load-from calib/calib_deeplabv3_mv2_512x512_5k_voc12aug_cityscapes/version_0/latest.pth \
    --cfg-options data.samples_per_gpu=8 \
    --seed 233 \
    --with_ASI True \
    --perplexity_pkl "perplexity/perplexity_hosvd_10L_deeplabv3_mv2_512x512_20k_cityscapes/perplexity_combined.pkl"\
    --budget 1.04174482822418