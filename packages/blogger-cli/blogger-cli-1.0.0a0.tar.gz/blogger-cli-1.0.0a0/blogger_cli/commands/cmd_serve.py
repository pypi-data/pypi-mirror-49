import os
import socketserver
import http.server

import click
from blogger_cli.cli import pass_context


@click.command('serve', short_help="Serve your blog locally")
@click.argument('blog', required=False )
@click.option('--port', '-p', 'port', type=int, default=8000)
@click.option('-dir', 'dir')
@click.option('-v', '--verbose', is_flag=True)
@pass_context
def cli(ctx, blog, port, dir,  verbose):
    ctx.verbose = verbose
    ctx.vlog("\n:: GOT blog:", blog, "port:", str(port), "(", type(port), ")")

    if not blog:
        blog = ctx.default_blog
        ctx.vlog(":: No blog name given using default blog:", str(blog))
    if not blog:
        ctx.log("Pass blog with -b option or set a default blog in configs")
        raise SystemExit("ERROR: BLOG NAME NOT GIVEN")

    blog_dir = ctx.config.read(key=blog + ':blog_dir')
    if dir:
        blog_dir = dir

    if not blog_dir:
        ctx.log("CNo blog_dir set blog_dir in config or use --dir option")
        raise SystemExit("ERROR: No folder specified")

    blog_dir = os.path.abspath(os.path.expanduser(blog_dir))
    ctx.vlog(":: Got blog_dir:", blog_dir)
    ctx.log(":: Serving at http://localhost:" + str(port) + '/')
    ctx.log(":: Exit using CTRL+C")
    serve_locally(blog_dir, port)


def serve_locally(dir, PORT):
    web_dir = dir
    os.chdir(web_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    httpd.serve_forever()
