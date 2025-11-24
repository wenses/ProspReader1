import flask, os
from flask import *
from flask import render_template as rt


    # pip install --upgrade pymupdf   ← make sure you're on latest

import fitz

    # ==================== EDIT THESE ====================
def replace(filename):
    INPUT_PDF  = filename
    OUTPUT_PDF = f"Translated - {filename}"

    REPLACEMENTS = {
    "CL111": "Communication Skills",
    "C111":"communication_skills",
    "DS112":"Development Perspectives I",
    "MT100":"Analysis",
    "CS151":"Computer Organization",
    "CS174":"Programming in C",
    "IS162":"Information Systems",
    "IS158":"System Maintenance",
    "CS173":"BusinessComputer Communications",
    "IS143":"Discrete Stuctures",
    "IS171":"Computer Networks",
    "CS175":"Programming in Java",
    "IS181":"Web Programming",
    "DS113":"Development Perspectives II"
    
    # add more here
}
    # ====================================================

    doc = fitz.open(INPUT_PDF)
    total_replacements = 0

    print(f"Processing {doc.page_count} pages...\n")

    for page in doc:
        for old_text, new_text in REPLACEMENTS.items():
            # Search for all occurrences
            found = page.search_for(old_text, quads=True)  # quads = better for rotated text
            
            for rect in found:
                # Option 1: Clean replacement using redact (works on ALL versions ≥1.20)
                # This removes old text + inserts new one perfectly
                print(rect.width)
                page.add_redact_annot(rect, text=new_text, align=fitz.TEXT_ALIGN_LEFT)

                total_replacements += 1

        # Apply all redactions on this page (removes old + draws new)
        page.apply_redactions()

    doc.save(OUTPUT_PDF, garbage=4, deflate=True, clean=True)
    doc.close()

    print(f"Done! {total_replacements} replacement(s) made.")
    print(f"Saved → {OUTPUT_PDF}")
app=Flask(__name__)

@app.route("/")

def index():

	return rt("index.html")


@app.route('/uploader',methods=['GET','POST'])

def uploader():

	if request.method=="POST":
		f=request.files["file"]

		
		f.save(f.filename)
		replace(f.filename)
		
	

	return send_file(f'Translated - {f.filename}',as_attachment=True)

@app.route("/gotoportfolio",methods=['GET','POST'])
def portfolio():

    return redirect("https://cybermaster43.vercel.app")
	
app.run(host="0.0.0.0",port=1234)