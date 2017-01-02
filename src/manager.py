import json
from subprocess import call


def build_template():
    path = "src/template/"

    # Read html template
    with open(path+"grid_block.html") as f_bloc, open(path+"modal.html") as f_modal, open(path+'main.html') as f_main:
        block_modal = "".join(f_modal.readlines())
        block_template = "".join(f_bloc.readlines())
        block_main = ''.join(f_main.readlines())

    # Read Data from json
    path = 'src/data/'
    with open(path+"projects.json") as f_proj, open(path+"tuto.json") as f_tuto:
        projects_data = json.loads("".join(f_proj.readlines()))
        tuto_data = json.loads("".join(f_tuto.readlines()))


    # Initialize html code for each template
    all_modal_html = ""
    all_project_html = ""
    all_tuto_html = ""


    # Build tuto
    for data in tuto_data.values():
        all_tuto_html += block_template.format(**data)
        path = data["path_modal"]
        if path.endswith(".md"):
            # Convert md to html
            out_path = path[:-2] + "html"
            call(["pandoc", path, "-o", out_path])
            path = out_path
        with open(path) as ff:
            modal_html = ''.join(ff.readlines())
        all_modal_html += block_modal.format(id=data["id"], type="tutorial",
                                             html=modal_html)

    # Build tuto
    for data in projects_data.values():
        all_project_html += block_template.format(**data)
        path = data["path_modal"]
        if path.endswith(".md"):
            # Convert md to html
            out_path = path[:-2] + "html"
            call(["pandoc", path, "-o", out_path])
            path = out_path
        with open(path) as ff:
            modal_html = ''.join(ff.readlines())
        all_modal_html += block_modal.format(id=data["id"], type="project",
                                             html=modal_html)

    # Write html in template
    html = block_main.format(portfolio_tuto=all_tuto_html,
                             portfolio_project=all_project_html,
                             html_modal=all_modal_html)
    with open("index.html", "w") as ff:
        ff.write(html)

if __name__ == '__main__':
    build_template()
