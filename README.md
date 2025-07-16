# Resume Creator

A flexible LaTeX resume generator that uses JSON data and Jinja2 templating to create resumes. Based on Jake's resume template. I built this application because it was tedious to manage multiple resumes for different applications.

## How to run? 

### Build the docker image

```bash
docker build . -t resume
```

### Run the application

Either run the provided script `build.sh` with
```bash
./build.sh
```
Or execute the command:

```bash
docker run -it \
--env-file .env \
-v $(pwd)/output:/output \
-v $(pwd)/src/resume_creator:/app/src/resume_creator \
resume
```
Note: It will take some time (a few minutes) to install the required tex packages.

To modify the content of the resume, edit `src/resume_creator/data/resume.json` and `src/resume_creator/templates/resume.tex`

### Privacy Controls

Set environment variables to control personal information:

```bash
export SHOW_PERSONAL_INFO=1
export PHONE="+1234567890"
export EMAIL="your.email@example.com"
```
Then follow the above steps to generate the resume with your phone number and email.

## Credits

Built on top of these LaTeX resume templates:
- [Jake's resume](https://github.com/jakegut/resume)
- [sb2nov's resume](https://github.com/sb2nov/resume/)