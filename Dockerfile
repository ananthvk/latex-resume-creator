FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY pyproject.toml pdm.lock* ./

# RUN python -m venv .venv
# RUN source .venv/bin/activate
RUN pip3 install --no-cache-dir jinja2 python-dotenv --break-system-packages

COPY src/ ./src/
COPY README.md ./

WORKDIR /app/src/resume_creator

CMD ["sh", "-c", "python main.py --stdout > /output/out.tex && pdflatex -output-directory=/output /output/out.tex"]