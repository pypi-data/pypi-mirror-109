# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
from fototex.foto import Foto

# foto = Foto("/home/benjamin/Documents/PRO/PRODUITS/SENTINEL"
#             "/S2A_MSIL1C_20201006T132241_N0209_R038_T23LKC_20201006T151824.SAFE/GRANULE"
#             "/L1C_T23LKC_A027634_20201006T132239/IMG_DATA/T23LKC_20201006T132241_B03.jp2",
#             in_memory=True, data_chunk_size=1000000)

foto = Foto("/home/benjamin/Documents/PRO/FOTO/001_DONNEES/planet_g_culdesac_clip_tampon_ndvi.tif")

# root = tkinter.Tk()
# plot(root, foto.dataset, foto.band, reduced_r_spectra, 0.6, 16, "max", 3, [2, 98])
# tkinter.mainloop()

# foto = Foto("/home/benjamin/Documents/PRO/FOTO/Images_entrées_fototex"
#             "/PAN_Mosaic_alizees_SEULEMENT.tif",
#             in_memory=False, data_chunk_size=2000000, method="moving")

foto.run(13, keep_dc_component=True, nb_processes=6)
# foto.out_dir = "/home/benjamin/Documents/PRO/PRODUITS/FOTO_RGB/SENTINEL"
foto.plot(nb_quadrants=8, norm_method="max")
# foto.plot("/home/benjamin/Documents/PRO/PRODUITS/FOTO_RGB/SENTINEL"
#           "/T23LKC_20201006T132241_B04_method=block_wsize=19_dc=True_foto_data.h5",
#           nb_quadrants=10, norm_method="max")
# foto.save_rgb()
# foto.save_data()
