# Markdown to Fluitopics command line tool

The idea of this tool is to be able to collect documentation written
as markdown files in a various places in a project and push it to
a [Fluitopics](https://www.fluidtopics.com/) portal.

The tool uses the FTML upload capability:

- https://doc.antidot.net/r/Upload-FTML-Content-to-Fluid-Topics/Configure-FTML-Content

## Features

- Collect any markdown file (.md) contained in a project
- Be able to select public vs internal content from [metadata contained
  in the markdown files](https://stackoverflow.com/questions/44215896/markdown-metadata-format).
- Build the FT TOC (ftmap) from metadata contained in the markdown files

## Documentation

You can find some explanations on how md2ft works [here](https://doc.antidot.net/r/Technical-Notes/Markdown-to-Fluid-Topics-md2ft).
