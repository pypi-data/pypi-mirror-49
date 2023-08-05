import os
import shutil
from base64 import b64decode
from pathlib import Path

from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen



def extract_and_write_static(ctx, html_body, topic_filename, blog_post_dir):
    global EXTRACT_LIST
    blog = ctx.current_blog
    EXTRACT_LIST = ctx.config.read(key=blog+':post_extract_list')
    if not EXTRACT_LIST:
        EXTRACT_LIST = ['URI', 'URL']

    static_dir = ctx.conversion['img_dir']
    topic = os.path.dirname(topic_filename)
    filename = os.path.basename(topic_filename)
    name, ext = os.path.splitext(filename)
    static_path = os.path.join(static_dir, topic, name)
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    soup = BS(html_body, 'html.parser')
    images = soup.find_all('img')
    ctx.log(":: Found", len(images), "images")
    extract_images(ctx, images, static_path, filename, blog_post_dir)

    videos = soup.find_all('video')
    extract_videos(ctx, videos, static_path, filename, blog_post_dir)
    ctx.log(":: Found", len(videos), "videos")

    if not os.listdir(static_path):
        os.rmdir(static_path)

    return soup.decode('utf8')


def extract_videos(ctx, videos, video_path, filename, blog_post_dir):
    for index, video_tag in enumerate(videos):
        try:
            video_data = video_tag['src']
        except:
            video_data = video_tag.source['src']

        try:
            video_name = video_tag['title'].strip().lower()
        except:
            video_name = None

        if not video_name:
            video_name = 'video_' + str(index+1)

        video_name = video_name.replace(' ', '_').replace('.','_') + '.mp4'
        video_path = os.path.join(video_path, video_name)

        if (video_data.startswith('data:video/mp4;base64,')
            and 'URI' in EXTRACT_LIST):

            ctx.log(":: Detected DATA URI video. Writing to", video_path)
            video_tag = extract_and_write_uri(video_data, video_tag, video_path,
                                        blog_post_dir)
        else:
            file_path = get_absolute_path(ctx, filename)
            dest_path = os.path.dirname(video_path)
            extracted_path = extract_static_files(video_data, file_path, dest_path)
            if extracted_path:
                new_video_src = get_static_src(blog_post_dir, video_path)
                video_tag['src'] = new_video_src


def extract_images(ctx, images, img_path, filename, blog_post_dir):
    for index, img_tag in enumerate(images):
        img_data = img_tag['src']
        try:
            image_name = img_tag['title'].strip().lower()
        except:
            image_name = None

        if not image_name:
            image_name = 'image_' + str(index+1)

        image_name = image_name.replace(' ','_').replace('.','_') + '.png'
        image_path = os.path.join(img_path, image_name)

        if (img_data.startswith('data:image/png;base64,')
            and 'URI' in EXTRACT_LIST):

            ctx.log(":: Detected DATA URI img. Writing to", image_path)
            img_tag = extract_and_write_uri(img_data, img_tag, image_path,
                                        blog_post_dir)
        elif ( (img_data.startswith('http') or img_data.startswith('https'))
                and 'URL' in EXTRACT_LIST):
            img_tag = extract_and_write_url_img(ctx, img_data, img_tag,
                                                image_path, blog_post_dir)
        else:
            file_path = get_absolute_path(ctx, filename)
            dest_path = os.path.dirname(image_path)
            extracted_path = extract_static_files(img_data, file_path, dest_path)
            if extracted_path:
                new_img_src = get_static_src(blog_post_dir, extracted_path)
                img_tag['src'] = new_img_src


def extract_and_write_uri(data, tag, static_path, blog_post_dir):
    __, encoded = data.split(",", 1)
    data = b64decode(encoded)
    with open(static_path, 'wb') as wf:
        wf.write(data)

    static_src = get_static_src(blog_post_dir, static_path)
    tag['src'] = static_src
    return tag


def extract_and_write_url_img(ctx, img_data, img_tag,
                            image_path, blog_post_dir):
    ctx.vlog(":: Downloading image from", img_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;Intel ' +
            'Mac OS X 10_10_1) AppleWebKit/537.36(KHTML, like Gecko)'+
            ' Chrome/39.0.2171.95 Safari/537.36'}
    try:
        req = Request(img_data, headers=headers)
        with urlopen(req) as response:
            raw_image = response.read()

        ctx.log(":: Detected url image. Writing to", image_path)
        with open(image_path, 'wb') as wf:
            wf.write(raw_image)

        image_src = get_static_src(blog_post_dir, image_path)
        img_tag['src'] = image_src
        ctx.vlog(":: Replacing source tag with:", image_src)
    except Exception as E:
        ctx.vlog(":: skipping  the image.", E)
        pass

    return img_tag


def get_static_src(destination_dir, static_path):
    os.chdir(destination_dir)
    src_path = os.path.relpath(static_path)
    return src_path


def get_absolute_path(ctx, filename):
    all_files = ctx.conversion['file_ext_map'].keys()
    file_path = [file for file in all_files if filename in file]
    return file_path[0]


def extract_static_files(data, file_path, dest_dir):
    orig_dir = Path(os.path.dirname(file_path))
    static_path = orig_dir /  data
    data = os.path.basename(data)

    if static_path.exists():
        static_path = static_path.resolve()
        dest_path = os.path.join(dest_dir, data)
        shutil.copyfile(str(static_path), dest_path)
        return dest_path
