import json
import os
import datetime

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render

from .core.main import main
from .forms import FontGenerationForm


def generate_font(request):
    if request.method == "POST":
        form = FontGenerationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded image
            image = form.cleaned_data["image_file"]
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, "uploads", image_name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Update config file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            year = datetime.datetime.now().year
            config_data = {
                "threshold_value": form.cleaned_data["threshold_value"],
                "props": {
                    "ascent": form.cleaned_data["ascent"],
                    "descent": form.cleaned_data["descent"],
                    "em": form.cleaned_data["em"],
                    "encoding": form.cleaned_data["encoding"],
                    "lang": form.cleaned_data["lang"],
                    "filename": form.cleaned_data["filename"],
                    "style": form.cleaned_data["style"],
                },
                "sfnt_names": {
                    "Copyright": f"Copyright (c) {year} by {form.cleaned_data['copyright']}",
                    "Family": form.cleaned_data["filename"],
                    "SubFamily": form.cleaned_data["style"],
                    "UniqueID": f"{form.cleaned_data['filename']} {date}",
                    "Fullname": f"{form.cleaned_data['filename']} {form.cleaned_data['style']}",
                    "Version": "Version 1.0",
                    "PostScriptName": f"{form.cleaned_data['filename']}-{form.cleaned_data['style']}",
                },
            }
            default_path = os.path.join(
                settings.BASE_DIR, "app", "core", "default.json"
            )
            with open(default_path, "r") as config_file:
                default = json.load(config_file)

            default.update(config_data)
            config_path = os.path.join(settings.MEDIA_ROOT, "config.json")
            with open(config_path, "w") as config_file:
                json.dump(default, config_file, indent=2)

            # Run the font generation
            output_dir = os.path.join(settings.MEDIA_ROOT, "fonts")
            os.makedirs(output_dir, exist_ok=True)
            main(image_path, output_dir, config=config_path)

            # Get the generated font file path
            font_name = form.cleaned_data["filename"]
            font_url = os.path.join(
                settings.MEDIA_URL, "fonts", f"{font_name}.ttf"
            ).replace("\\", "/")
            return render(
                request,
                "app/success.html",
                {"download_url": font_url, "font_name": font_name},
            )
    else:
        form = FontGenerationForm()
    return render(request, "app/generate.html", {"form": form})


def download_sample(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "sample.pdf")
    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename="sample.pdf"
    )
