# %%


# %%
import glob
import os
import shutil
import zipfile
import requests
from config import config_vars

# %% [markdown]
# # Download zip files from BBBC website

# %%
images = requests.get('https://data.broadinstitute.org/bbbc/BBBC039/images.zip')
masks = requests.get('https://data.broadinstitute.org/bbbc/BBBC039/masks.zip')
metadata = requests.get('https://data.broadinstitute.org/bbbc/BBBC039/metadata.zip')

# %%
assert images.ok
assert masks.ok
assert metadata.ok

# %% [markdown]
# # Extract images

# %%
print('getcwd:      ', os.getcwd())
print(config_vars['raw_images_dir'])
images_zip = os.path.join(config_vars['raw_images_dir'], 'images.zip')
os.makedirs(config_vars['raw_images_dir'], exist_ok=True)
with open(images_zip, 'wb') as f:
    f.write(images.content)
    
zip_ref = zipfile.ZipFile(images_zip, 'r')
for file in zip_ref.namelist():
    if file.startswith('images/'):
        zip_ref.extract(file, config_vars['raw_images_dir'])

zip_ref.close()
os.remove(images_zip)

for file in glob.glob(os.path.join(config_vars['raw_images_dir'], 'images/*')):
    shutil.move(file, config_vars['raw_images_dir'])

shutil.rmtree(os.path.join(config_vars['raw_images_dir'], 'images'))

# %% [markdown]
# # Extract annotations

# %%
masks_zip = os.path.join(config_vars['raw_annotations_dir'], 'masks.zip')
os.makedirs(config_vars['raw_annotations_dir'], exist_ok=True)
with open(masks_zip, 'wb') as f:
    f.write(masks.content)

zip_ref = zipfile.ZipFile(masks_zip, 'r')
for file in zip_ref.namelist():
    if file.startswith('masks/'):
        zip_ref.extract(file, config_vars['raw_annotations_dir'])

zip_ref.close()
os.remove(masks_zip)

for file in glob.glob(os.path.join(config_vars['raw_annotations_dir'], 'masks/*')):
    shutil.move(file, config_vars['raw_annotations_dir'])
shutil.rmtree(os.path.join(config_vars['raw_annotations_dir'], 'masks'))

# %% [markdown]
# # Extract metadata

# %%
metadata_zip = os.path.join(config_vars['root_directory'], 'metadata.zip')
with open(metadata_zip, 'wb') as f:
    f.write(metadata.content)

zip_ref = zipfile.ZipFile(metadata_zip, 'r')
for file in zip_ref.namelist():
    if file.startswith('metadata/'):
        zip_ref.extract(file, config_vars['root_directory'])

zip_ref.close()
os.remove(metadata_zip)

for file in glob.glob(os.path.join(config_vars['root_directory'], 'metadata/*')):
    shutil.move(file, config_vars['root_directory'])
shutil.rmtree(os.path.join(config_vars['root_directory'], 'metadata'))

# %%



