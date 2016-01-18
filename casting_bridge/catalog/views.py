# -*- coding: utf-8 -*-
import os
from functools import wraps
from werkzeug import secure_filename
from flask import request, Blueprint, render_template, jsonify, flash, \
    redirect, url_for
from casting_bridge import db, app, ALLOWED_EXTENSIONS, manager, admin
#from casting_bridge import manager
from casting_bridge.catalog.models import Classifier, Person, Skill, Document, UserForm, SelectMultipleFieldNoValidate, UpdateForm
from sqlalchemy.orm.util import join
from flask.ext.admin.contrib.sqla import ModelView
from datetime import datetime
import pytz
import helpers

catalog = Blueprint('catalog', __name__)

def allowed_file(filename):
    return '.' in filename and \
            filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def template_or_json(template=None):
    """"Return a dict from your view and this will either
    pass it to a template or render json. Use like:

    @template_or_json('template.html')
    """
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_xhr or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@catalog.route('/')
@catalog.route('/data-enter', methods=['GET', 'POST'])
def create_enter():
    form = UserForm(request.form)

    choices = list()
    want_participate_box = Classifier.query.filter_by(category='want_participate').all()
    for want_participate_box in want_participate_box:
        if want_participate_box:
            choices.append((want_participate_box.tag_lv,want_participate_box.tag_lv))
    form.want_participate.choices = choices

    choices = []
    city_box = Classifier.query.filter_by(category='city').all()
    for city_box in city_box:
        if city_box:
            choices.append((city_box.tag_lv,city_box.tag_lv))
    form.city.choices = choices

    choices = []
    haircolor = Classifier.query.filter_by(category='haircolor').all()
    for haircolor in haircolor:
        if haircolor:
            choices.append((haircolor.tag_lv,haircolor.tag_lv))
    form.haircolor.choices = choices

    choices = []
    eyecolor = Classifier.query.filter_by(category='eyecolor').all()
    for eyecolor in eyecolor:
        if eyecolor:
            choices.append((eyecolor.tag_lv,eyecolor.tag_lv))
    form.eyecolor.choices = choices

    choices = []
    voice = Classifier.query.filter_by(category='voice').all()
    for voice in voice:
        if voice:
            choices.append((voice.tag_lv,voice.tag_lv))
    form.voice.choices = choices

    choices = []
    co = Classifier.query.filter_by(category='current_occupation').all()
    for co in co:
        if co:
            choices.append((co.tag_lv,co.tag_lv))
    form.current_occupation.choices = choices

    choices = []
    for size in range(35,50,1): # filled clothe size range 35 to 49
        choices.append((str(size),(str(size))))
    form.foot_size.choices = choices

    choices = []
    for size in range(32,69,2): # filled clothe size range 32 to 68
        choices.append((str(size),(str(size))))
    form.cloth_size.choices = choices

    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        nickname = form.nickname.data
        pcode = form.pcode.data
        passport_nr = form.passport_nr.data
        birthdate = form.birthdate.data
        my_phone_code = form.my_phone_code.data
        my_phone = form.my_phone.data
        email = form.email.data
        other_phone_code = form.other_phone_code.data
        other_phone = form.other_phone.data
        home_address = form.home_address.data
        height = form.height.data
        foot_size = form.foot_size.data
        cloth_size = form.cloth_size.data
        voice = form.voice.data
        race = form.race.data
        contact_lenses = form.contact_lenses.data
        be_dressed = form.be_dressed.data
        species = form.species.data
        mother_phone_code = form.mother_phone_code.data
        mother_phone = form.mother_phone.data
        mother_name = form.mother_name.data
        father_phone_code = form.father_phone_code.data
        father_phone = form.father_phone.data
        father_name = form.father_name.data
        speciality = form.speciality.data
        experience = form.experience.data
        city = form.city.data
        haircolor = form.haircolor.data
        eyecolor = form.eyecolor.data
        current_occupation = form.current_occupation.data
        workplace = form.workplace.data
        person = Person(datetime.now(pytz.timezone("Europe/Riga")), datetime.now(pytz.timezone("Europe/Riga")), name, surname, nickname, pcode, passport_nr, birthdate, my_phone_code, my_phone, email, other_phone_code, other_phone, home_address, height, foot_size, cloth_size, voice, race, contact_lenses, be_dressed, None, False, species, mother_phone_code, mother_phone, mother_name, father_phone_code, father_phone, father_name, speciality, experience, None, current_occupation, workplace)
        db.session.add(person)
        db.session.commit()
        skills = list()

        if city:
            skills.append(['city', city])

        if haircolor:
            skills.append(['haircolor', haircolor])

        if eyecolor:
            skills.append(['eyecolor', eyecolor])

        for subspeciality in form.subspeciality.data:
            skills.append(['subspeciality', subspeciality])

        for danceskill in form.danceskill.data:
            skills.append(['danceskill', danceskill])

        for singskill in form.singskill.data:
            skills.append(['singskill', singskill])

        for musicskill in form.musicskill.data:
            skills.append(['musicskill', musicskill])

        for sportskill in form.sportskill.data:
            skills.append(['sportskill', sportskill])

        for swimskill in form.swimskill.data:
            skills.append(['swimskill', swimskill])

        for otherskill in form.otherskill.data:
            skills.append(['otherskill', otherskill])

        for driveskill in form.driveskill.data:
            skills.append(['driveskill', driveskill])

        for languageskill in form.languageskill.data:
            skills.append(['languageskill', languageskill])

        for want_participate in form.want_participate.data:
            skills.append(['want_participate', want_participate])

        for dont_want_participate in form.dont_want_participate.data:
            skills.append(['dont_want_participate', dont_want_participate])

        for interested_in in form.interested_in.data:
            skills.append(['interested_in', interested_in])

        for tattoo in form.tattoo.data:
            skills.append(['tattoo', tattoo])

        for piercing in form.piercing.data:
            skills.append(['piercing', piercing])

        for afraidof in form.afraidof.data:
            skills.append(['afraidof', afraidof])

        for religion in form.religion.data:
            skills.append(['religion', religion])

        for educational_institution in form.educational_institution.data:
            skills.append(['educational_institution', educational_institution])

        for learned_profession in form.learned_profession.data:
            skills.append(['learned_profession', learned_profession])

        for degree in form.degree.data:
            skills.append(['degree', degree])

        for skill in skills:
            #flash('Skills [%s] [%s]' % (skill[0], skill[1]), 'success')
            item = Classifier.query.filter_by(category=skill[0], tag_lv = skill[1].capitalize()).first()
            if item is None: # add new entry in Classifier
                item = Classifier(category=skill[0], tag_lv=skill[1].capitalize())
                db.session.add(item)
                db.session.commit()

            add_skill = Skill(person=person, classifier=item)
            db.session.add(add_skill)
            db.session.commit()

        helpers.file_upload('photo', 'image1', person.id)
        helpers.file_upload('photo', 'image2', person.id)
        profile_image = request.files['profile_image']
        cv = request.files['cv']
        filename = ''
        if profile_image and helpers.allowed_file(profile_image.filename):
            #flash('profile_image: [%s]' % profile_image, 'success')
            filename, file_extension = os.path.splitext(secure_filename(profile_image.filename))
            filename = str(person.id) + "_profile" + file_extension
            profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Person.query.filter_by(id=person.id).update({
                'profile_image': filename
            })
        if cv and helpers.allowed_file(cv.filename):
            #flash('profile_image: [%s]' % profile_image, 'success')
            filename, file_extension = os.path.splitext(secure_filename(cv.filename))
            filename = str(person.id) + "_cv" + file_extension
            cv.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Person.query.filter_by(id=person.id).update({
                'cv': filename
            })

        db.session.commit()

        flash(
            'The person %s has been created' % person.id, 'success'
        )

        return redirect(
            url_for('catalog.profiles')
        )

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('data-enter.html', form=form)

@catalog.route('/update-profile/<id>', methods=['GET', 'POST'])
def update_profile(id):
    person = Person.query.get_or_404(id)
    form = UpdateForm(
        request.form,
        name=person.name,
        surname=person.surname,
        nickname=person.nickname,
        pcode=person.pcode,
        passport_nr=person.passport_nr,
        birthdate=person.birthdate,
        my_phone=person.my_phone,
        email=person.email,
        other_phone=person.other_phone,
        home_address=person.home_address,
        height=person.height,
        foot_size=person.foot_size,
        cloth_size=person.cloth_size,
        voice=person.voice,
        race=person.race,
        contact_lenses=person.contact_lenses,
        be_dressed=person.be_dressed,
        mother_phone_code=person.mother_phone_code,
        mother_phone=person.mother_phone,
        mother_name=person.mother_name,
        father_phone_code=person.father_phone_code,
        father_phone=person.father_phone,
        father_name=person.father_name,
        experience=person.experience,
        current_occupation = person.current_occupation,
        workplace = person.workplace
    )

    if person.species:
        form.species.data=person.species

    if person.speciality:
        form.speciality.data=person.speciality

    # Get all possible values(choices) from Classifier
    choices = list()
    city_box = Classifier.query.filter_by(category='city').all()
    for city_box in city_box:
        if city_box:
            choices.append((city_box.tag_lv,city_box.tag_lv))
    form.city.choices = choices

    choices = []
    haircolor = Classifier.query.filter_by(category='haircolor').all()
    for haircolor in haircolor:
        if haircolor:
            choices.append((haircolor.tag_lv,haircolor.tag_lv))
    form.haircolor.choices = choices

    choices = []
    eyecolor = Classifier.query.filter_by(category='eyecolor').all()
    for eyecolor in eyecolor:
        if eyecolor:
            choices.append((eyecolor.tag_lv,eyecolor.tag_lv))
    form.eyecolor.choices = choices

    choices = []
    voice = Classifier.query.filter_by(category='voice').all()
    for voice in voice:
        if voice:
            choices.append((voice.tag_lv,voice.tag_lv))
    form.voice.choices = choices

    choices = []
    co = Classifier.query.filter_by(category='current_occupation').all()
    for co in co:
        if co:
            choices.append((co.tag_lv,co.tag_lv))
    form.current_occupation.choices = choices

    choices = []
    for size in range(35,50,1): # filled clothe size range 35 to 49
        choices.append((str(size),(str(size))))
    form.foot_size.choices = choices

    choices = []
    for size in range(32,69,2): # filled clothe size range 32 to 68
        choices.append((str(size),(str(size))))
    form.cloth_size.choices = choices

    # Get all assigned Skills for person and add them as selected in form.
    classifiers = Classifier.query.select_from(join(Classifier, Skill)).filter(Skill.person_id == id)
    skill_box = {}
    for item in classifiers:
        #flash('skill [%s] cat [%s] ' % (item.tag_lv, item.category), 'info')
        if skill_box.get(item.category) is None:
            skill_box[item.category] = [(item.tag_lv,item.tag_lv)]
        else:
            skill_box[item.category].append((item.tag_lv,item.tag_lv))

    #flash('danceskilldanceskill [%s]' % skill_box.get('danceskill'), 'info')
    if skill_box.get('city'):
        for skill in skill_box.get('city'):
            form.city.data= skill[0]
    if skill_box.get('haircolor'):
        for skill in skill_box.get('haircolor'):
            form.haircolor.data= skill[0]
    if skill_box.get('eyecolor'):
        for skill in skill_box.get('eyecolor'):
            form.eyecolor.data= skill[0]
    if skill_box.get('subspeciality'):
        form.subspeciality.choices = skill_box.get('subspeciality')
    if skill_box.get('danceskill'):
        form.danceskill.choices = skill_box.get('danceskill')
    if skill_box.get('singskill'):
        form.singskill.choices = skill_box.get('singskill')
    if skill_box.get('musicskill'):
        form.musicskill.choices = skill_box.get('musicskill')
    if skill_box.get('sportskill'):
        form.sportskill.choices = skill_box.get('sportskill')
    if skill_box.get('swimskill'):
        form.swimskill.choices = skill_box.get('swimskill')
    if skill_box.get('driveskill'):
        form.driveskill.choices = skill_box.get('driveskill')
    if skill_box.get('languageskill'):
        form.languageskill.choices = skill_box.get('languageskill')
    if skill_box.get('otherskill'):
        form.otherskill.choices = skill_box.get('otherskill')
    if skill_box.get('want_participate'):
        form.want_participate.choices = skill_box.get('want_participate')
    if skill_box.get('dont_want_participate'):
        form.dont_want_participate.choices = skill_box.get('dont_want_participate')
    if skill_box.get('interested_in'):
        form.interested_in.choices = skill_box.get('interested_in')
    if skill_box.get('tattoo'):
        form.tattoo.choices = skill_box.get('tattoo')
    if skill_box.get('piercing'):
        form.piercing.choices = skill_box.get('piercing')
    if skill_box.get('afraidof'):
        form.afraidof.choices = skill_box.get('afraidof')
    if skill_box.get('religion'):
        form.religion.choices = skill_box.get('religion')
    if skill_box.get('educational_institution'):
        form.educational_institution.choices = skill_box.get('educational_institution')
    if skill_box.get('learned_profession'):
        form.learned_profession.choices = skill_box.get('learned_profession')
    if skill_box.get('degree'):
        form.degree.choices = skill_box.get('degree')
    if skill_box.get('current_occupation'):
        form.current_occupation.choices = skill_box.get('current_occupation')
    if skill_box.get('voice'):
        form.current_occupation.choices = skill_box.get('voice')
    if skill_box.get('cb_tags'):
        form.cb_tags.choices = skill_box.get('cb_tags')

    photos = Document.query.filter_by(person_id=id, type='photo').paginate(1,100,error_out=False)
    #for photo in photos:
    #    flash("photo : [%s]" % photo.name, 'info')

    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        nickname = form.nickname.data
        pcode = form.pcode.data
        passport_nr = form.passport_nr.data
        birthdate = form.birthdate.data
        my_phone = form.my_phone.data
        email = form.email.data
        other_phone = form.other_phone.data
        home_address = form.home_address.data
        height = form.height.data
        foot_size = request.form['foot_size']
        cloth_size = request.form['cloth_size']
        voice = request.form['voice']
        race = form.race.data
        contact_lenses = form.contact_lenses.data
        be_dressed = form.be_dressed.data
        # field is set from request.form['species'], because form.species.data is alredy set to (old)value from db
        species = request.form['species']
        mother_phone_code = form.mother_phone_code.data
        mother_phone = form.mother_phone.data
        mother_name = form.mother_name.data
        father_phone_code = form.father_phone_code.data
        father_phone = form.father_phone.data
        father_name = form.father_name.data
        speciality = request.form['speciality']
        experience = form.experience.data
        city = request.form['city']
        haircolor = request.form['haircolor']
        eyecolor = request.form['eyecolor']
        current_occupation = request.form['current_occupation']
        workplace = form.workplace.data

        Person.query.filter_by(id=id).update({
            'modified': datetime.now(pytz.timezone("Europe/Riga")),
            'name': name,
            'surname': surname,
            'nickname': nickname,
            'pcode': pcode,
            'passport_nr': passport_nr,
            'birthdate': birthdate,
            'my_phone': my_phone,
            'email': email,
            'other_phone': other_phone,
            'home_address': home_address,
            'height': height,
            'foot_size': foot_size,
            'cloth_size': cloth_size,
            'voice': voice,
            'race': race,
            'contact_lenses': contact_lenses,
            'be_dressed': be_dressed,
            'species': species,
            'mother_phone_code': mother_phone_code,
            'mother_phone': mother_phone,
            'mother_name': mother_name,
            'father_phone_code': father_phone_code,
            'father_phone': father_phone,
            'father_name': father_name,
            'speciality': speciality,
            'experience': experience,
            'current_occupation': current_occupation,
            'workplace': workplace
        })

        skills = list()
        if city:
            skills.append(['city', city])

        if haircolor:
            skills.append(['haircolor', haircolor])

        if eyecolor:
            skills.append(['eyecolor', eyecolor])

        for subspeciality in form.subspeciality.data:
            skills.append(['subspeciality', subspeciality])

        for danceskill in form.danceskill.data:
            skills.append(['danceskill', danceskill])

        for singskill in form.singskill.data:
            skills.append(['singskill', singskill])

        for musicskill in form.musicskill.data:
            skills.append(['musicskill', musicskill])

        for sportskill in form.sportskill.data:
            skills.append(['sportskill', sportskill])

        for swimskill in form.swimskill.data:
            skills.append(['swimskill', swimskill])

        for otherskill in form.otherskill.data:
            skills.append(['otherskill', otherskill])

        for driveskill in form.driveskill.data:
            skills.append(['driveskill', driveskill])

        for languageskill in form.languageskill.data:
            skills.append(['languageskill', languageskill])

        for want_participate in form.want_participate.data:
            skills.append(['want_participate', want_participate])

        for dont_want_participate in form.dont_want_participate.data:
            skills.append(['dont_want_participate', dont_want_participate])

        for interested_in in form.interested_in.data:
            skills.append(['interested_in', interested_in])

        for tattoo in form.tattoo.data:
            skills.append(['tattoo', tattoo])

        for piercing in form.piercing.data:
            skills.append(['piercing', piercing])

        for afraidof in form.afraidof.data:
            skills.append(['afraidof', afraidof])

        for religion in form.religion.data:
            skills.append(['religion', religion])

        for educational_institution in form.educational_institution.data:
            skills.append(['educational_institution', educational_institution])

        for learned_profession in form.learned_profession.data:
            skills.append(['learned_profession', learned_profession])

        for degree in form.degree.data:
            skills.append(['degree', degree])

        for cb_tags in form.cb_tags.data:
            skills.append(['cb_tags', cb_tags])

        # Delete outdated skills
        Skill.query.filter_by(person_id=id).delete()
        for skill in skills:
            #flash('Skills [%s] [%s]' % (skill[0], skill[1]), 'success')
            item = Classifier.query.filter_by(category=skill[0], tag_lv = skill[1].capitalize()).first()
            if item is None: # add new entry in Classifier
                item = Classifier(category=skill[0], tag_lv=skill[1].capitalize())
                db.session.add(item)

            add_skill = Skill(person=person, classifier=item)
            db.session.add(add_skill)

        db.session.commit()

        files = request.files.getlist('images[]')
        for file in files:
            #flash('file: [%s]' % file.filename, 'success')
            filename = ''
            if file and allowed_file(file.filename):
                filename = str(person.id) + "_" + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                add_document = Document(datetime.now(pytz.timezone("Europe/Riga")), person.id, 'photo', filename)
                db.session.add(add_document)

        #helpers.file_upload('photo', 'image1', person.id)
        #helpers.file_upload('photo', 'image2', person.id)
        #helpers.file_upload('photo', 'image3', person.id)
        #helpers.file_upload('photo', 'image4', person.id)
        #helpers.file_upload('photo', 'image5', person.id)
        helpers.file_upload('audio', 'audio', person.id)
        helpers.file_upload('video', 'video', person.id)
        profile_image = request.files['profile_image']
        cv = request.files['cv']
        filename = ''
        if profile_image and helpers.allowed_file(profile_image.filename):
            #flash('profile_image: [%s]' % profile_image, 'success')
            filename, file_extension = os.path.splitext(secure_filename(profile_image.filename))
            filename = str(person.id) + "_profile" + file_extension
            profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Person.query.filter_by(id=person.id).update({
                'profile_image': filename
            })
        if cv and helpers.allowed_file(cv.filename):
            #flash('profile_image: [%s]' % profile_image, 'success')
            filename, file_extension = os.path.splitext(secure_filename(cv.filename))
            filename = str(person.id) + "_cv" + file_extension
            cv.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Person.query.filter_by(id=person.id).update({
                'cv': filename
            })

        db.session.commit()

        flash('Profile updated.', 'info')
        return redirect(url_for('catalog.profiles'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('profile_update.html', form=form, person=person, photos=photos )

@catalog.route('/profiles')
@catalog.route('/profiles/<int:page>')
def profiles(page=1):

    name = request.args.get('name')
    surname = request.args.get('surname')

    profiles = Person.query
    if name:
        profiles = profiles.filter(Person.name.like('%' + name + '%'))
    if surname:
        profiles = profiles.filter(Person.surname.like('%' + surname + '%'))

    return render_template(
        'profiles.html', profiles=profiles.paginate(page, 12)
    )

@catalog.route('/profile-delete')
def profile_delete():
    id = request.args.get('id')
    person = Person.query.get_or_404(id)

    # Delete documents and filse
    documents = Document.query.filter_by(person_id=id)
    for document in documents:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], document.name)
        #flash('filename [%s]' % (filename), 'success')
        if os.path.exists(filename):
            os.remove(filename)
    Document.query.filter_by(person_id=id).delete()

    # Delete skills
    Skill.query.filter_by(person_id=id).delete()

    # Delete profile picture
    if person.profile_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], person.profile_image)
        if os.path.exists(filename):
            os.remove(filename)
    # Delete person
    db.session.delete(person)
    db.session.commit()

    flash('Profile for %s %s deleted.' % (person.name, person.surname), 'info')

    return redirect(url_for('catalog.profiles'))

@catalog.route('/photo-delete')
def photo_delete():
    person_id = request.args.get('person_id')
    photo_id = request.args.get('photo_id')
    photo = Document.query.get_or_404(photo_id)
    filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.name)
    if os.path.exists(filename):
        os.remove(filename)
    db.session.delete(photo)
    db.session.commit()

    return redirect(url_for('catalog.update_profile', id=person_id))

manager.create_api(Classifier, methods=['GET'], results_per_page=None, exclude_columns=['skills'])

admin.add_view(ModelView(Classifier, db.session))

