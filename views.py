from bson import ObjectId
from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from website.models import Note
import json
# from website import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note_content = request.form.get('note')

        if len(note_content) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(current_app.db )
            new_note_data = {
                'data': note_content,
                'user_id': current_user.get_id()
            }
            new_note.add_note(new_note_data)
            flash('Note added!', category='success')

    new_note = Note(current_app.db)
    user_notes = new_note.get_all_notes(current_user.get_id())
    
    return render_template('home.html', user=current_user, notes=user_notes)



@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note.get('noteId')
    note = current_app.db.notes.find_one({"_id": ObjectId(noteId)})
    if note:
        if note['user_id'] == current_user.id:
            current_app.db.notes.delete_one({"_id": ObjectId(noteId)})
            
    return jsonify({})



# @views.route('/add-note', methods=['GET', 'POST'])
# @login_required
# def add_note():
#     note = request.form.get('note')
#     if len(note) < 1:
#         flash('Note is too short!', category='error')
#     else:
#         note_instance = Note(current_app.db)
#         note_instance.add_note(note)
#         flash('Note added!', category='success')

#     return redirect(url_for('views.home'))