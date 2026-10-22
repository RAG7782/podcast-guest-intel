## en.json

```json
{
  "locale": "en",
  "needs_native_review": false,
  "text_version": "en/v1",
  "form": {
    "validation": {
      "phone": "Type the number with country and area code, e.g. +1 415 555 2671."
    },
    "title": "Guest of {{show.name}}",
    "description_essencial": "Takes about 2 minutes. It helps us prepare a good conversation for you, with no surprises.",
    "description_completo": "Takes about 8 minutes. Almost everything is optional: skip whatever you prefer.",
    "confirmation": "Thank you! If you allowed email, the guest kit is on its way. To send files (PDFs, slides, photos), just reply to that email with attachments.",
    "sections": {
      "about": "About you",
      "content": "The conversation",
      "logistics": "Recording",
      "channels": "How we reach you",
      "consent": "Your data and this interview",
      "sensitive": "Sensitive data (optional)",
      "localization": "Other languages (optional)"
    },
    "fields": {
      "guest.full_name": { "title": "Full name", "help": "" },
      "guest.preferred_name": { "title": "What should we call you on air?", "help": "E.g. Ana, Dr. Ana, Professor Silva." },
      "guest.name_pronunciation": { "title": "How is your name pronounced?", "help": "Only if we might get it wrong." },
      "guest.pronouns": { "title": "Pronouns", "help": "Optional. E.g. she/her." },
      "guest.role_title": { "title": "Role or occupation", "help": "" },
      "guest.photo_url": { "title": "Link to a photo of you for promotion", "help": "Optional. A public link (website, LinkedIn, shared Drive)." },
      "bio.short": { "title": "Short bio, up to 2 lines", "help": "This is what we read in the intro." },
      "bio.long": { "title": "Full bio", "help": "Optional." },
      "links": { "title": "Your main links", "help": "Website, profiles, portfolio. One per line. If you have none, leave it blank." },
      "social_handles": { "title": "Handles to tag when we promote", "help": "One per line, as network: @user (e.g. instagram: @ana)." },
      "previous_interviews": { "title": "Interviews you have given", "help": "Links, one per line. Helps us avoid repeating questions." },
      "key_ideas": { "title": "Up to 3 ideas you want the audience to take away", "help": "One per line." },
      "stories_to_tell": { "title": "Stories you like to tell", "help": "One per line." },
      "controversies.accepts": { "title": "Controversial topics you are happy to discuss", "help": "One per line." },
      "controversies.declines": { "title": "Controversial topics you would rather avoid", "help": "One per line." },
      "off_limits_topics": { "title": "Off-limits topics", "help": "We will not touch these. One per line." },
      "wants_to_promote": { "title": "Anything you want to promote?", "help": "Book, course, event, project. One per line." },
      "dream_questions": { "title": "Questions you would love to be asked", "help": "One per line." },
      "conflicts_of_interest.details": { "title": "Conflicts of interest or sponsorships related to the topics", "help": "Leave blank if none." },
      "companion.name": { "title": "Bringing someone along? Who?", "help": "Leave blank if coming alone." },
      "materials": { "title": "Supporting materials (links)", "help": "Talks, books, articles, videos. One link per line. Files: reply to the kit email with attachments." },
      "recording_mode": { "title": "How will we record?", "help": "" },
      "scheduled_at": { "title": "Date and time already agreed with us", "help": "Only if already agreed. Used for the calendar invite and the day-before reminder." },
      "wants_prepublication_review": { "title": "Would you like to see the episode before we publish?", "help": "" },
      "preferred_channel": { "title": "Preferred channel to reach you", "help": "" },
      "contacts.email": { "title": "Your email", "help": "" },
      "invite.token": { "title": "Invitation code", "help": "Filled in by the link in the invitation email you received. Do not change it. If it is empty, submit anyway: the show will check with you before sending anything." },
      "contacts.whatsapp": { "title": "Your WhatsApp", "help": "Optional. With country code, e.g. +44 7700 900123." },
      "automation_consents": { "title": "May we use these channels to send you the kit and reminders?", "help": "Tick only what you want. Nothing ticked = nothing sent through that channel." },
      "image_voice": { "title": "Image and voice", "help": "" },
      "consent.general": { "title": "Consent", "help": "" },
      "consent.public_research": { "title": "Research in public sources", "help": "" },
      "consent.divulgacao": { "title": "Promotion (optional)", "help": "" },
      "accessibility.needs": { "title": "SENSITIVE DATA — Do you need any accessibility accommodation?", "help": "Optional. It may reveal health information: it is only used if you tick the consent right below." },
      "accessibility.accept": { "title": "SENSITIVE DATA — Specific consent (accessibility)", "help": "" },
      "sensitive.category": { "title": "SENSITIVE DATA — What is it about?", "help": "Optional." },
      "sensitive.value": { "title": "SENSITIVE DATA — What you want us to know", "help": "Optional. Write only what you want in the preparation." },
      "sensitive.accept": { "title": "SENSITIVE DATA — Specific consent", "help": "" },
      "localization.translation_text": { "title": "Translated subtitles and texts", "help": "" },
      "localization.dub_generic_voice": { "title": "Dubbing with a generic synthetic voice", "help": "" },
      "localization.dub_voice_replica": { "title": "SENSITIVE DATA — Artificial replica of your voice", "help": "" }
    },
    "choices": {
      "recording_mode": { "presencial": "In person, at the studio", "remoto": "Remote, online" },
      "yes_no": { "yes": "Yes", "no": "No" },
      "preferred_channel": { "email": "Email", "whatsapp": "WhatsApp", "phone": "Phone", "other": "Other" },
      "channels": {
        "email": "Email: guest kit and a day-before reminder",
        "whatsapp": "WhatsApp: kit and a day-before reminder",
        "calendar": "Calendar: invite with date and address"
      },
      "sensitive_category": {
        "origem_racial_etnica": "Racial or ethnic origin",
        "conviccao_religiosa": "Religious belief",
        "opiniao_politica": "Political opinion",
        "filiacao_sindical_religiosa_filosofica_politica": "Trade union or religious, philosophical or political membership",
        "saude": "Health",
        "vida_sexual": "Sex life",
        "genetico": "Genetic data",
        "biometrico": "Biometric data"
      }
    }
  },
  "consent": {
    "contact_email": "by email at {{email}}",
    "contact_reply_to_email": "by replying to any email from this show (including the invitation or the guest kit)",
    "clauses": {
      "BR-LGPD": {
        "clause_id": "BR-LGPD/v1",
        "legal_review": "pending",
        "text": "{{controller.name}} (data controller{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contact: {{controller.contact}}) will use the answers to this form only for the purposes below, related to your interview on {{show.name}}: {{purposes}}.\n\nTo prepare better questions, we will also look at information you have made public yourself (website, social media, interviews and published texts). Everything that goes into the preparation material will cite its source.\n\nWe will not use or keep sensitive data (health, religion, political opinion, sex life, racial or ethnic origin, among others) unless you write it yourself in the optional sensitive-data section and tick the specific consent for each item. It is your decision.\n\nThe data is deleted within {{retention_days}} days after the episode is published; we keep only the record of this consent, as proof. At any time and free of charge you may request access, correction or deletion, or withdraw this consent, {{controller.contact}}. If you do not want to consent, simply do not submit the form: the interview can still happen without it."
      },
      "EU-GDPR": {
        "clause_id": "EU-GDPR/v1",
        "legal_review": "pending",
        "text": "{{controller.name}} (data controller{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contact: {{controller.contact}}) will process the answers to this form based on your consent, only for: {{purposes}}.\n\nWe will also look at information you have made publicly accessible (website, social media, interviews, published texts), always citing the source.\n\nSpecial categories of data (health, religion, political opinion, sex life, racial or ethnic origin, among others) are processed only if you write them in the optional section and give explicit consent for each item.\n\nThe data is deleted within {{retention_days}} days after the episode is published. You have the right of access, rectification, erasure, restriction, portability and objection, and you may withdraw consent at any time ({{controller.contact}}) without affecting processing already carried out. You may also lodge a complaint with a supervisory authority."
      },
      "other": {
        "clause_id": "other/v1",
        "legal_review": "pending",
        "text": "{{controller.name}} (contact: {{controller.contact}}) will use the answers to this form only for: {{purposes}}. We will also look at information you have made public, always citing the source. Sensitive data is used only if you write it in the optional section and tick the specific consent. The data is deleted within {{retention_days}} days after publication. To access, correct, delete or withdraw consent: {{controller.contact}}."
      }
    },
    "purposes": {
      "preparo_entrevista": "preparing your interview",
      "dossie": "building the preparation material (with sources)",
      "memoria_episodio": "recording the episode in the show's archive",
      "divulgacao": "promoting the episode with your short bio, photo and handle"
    },
    "draft_notice": "NOTICE: this consent text is a DRAFT (v0) under legal review and may change. If the final version changes anything, we will ask for your consent again.",
    "general_accept": "I have read the text above and agree to the use of my answers for these purposes.",
    "public_research_accept": "I understand that information I have made public myself will be consulted, always citing the source.",
    "divulgacao_accept": "I also allow my short bio, photo and handle to be used to promote the episode.",
    "image_voice_accept": "I authorise the recording and publication of my image and voice in this episode.",
    "sensitive_intro": "This section is entirely optional and the decision is yours. Everything here is SENSITIVE DATA: it is used only if you write it and tick the specific consent right below each field. Without consent the information is discarded and not kept.",
    "sensitive_accept": "SENSITIVE DATA — I give specific, explicit consent to the use of the information I wrote above only to prepare and conduct this interview.",
    "accessibility_accept": "SENSITIVE DATA (may reveal health) — I allow the accessibility need above to be used only to organise the recording logistics.",
    "sensitive_purpose": "prepare and conduct this interview",
    "accessibility_purpose": "organise the recording logistics",
    "localization_intro": "This section is optional and each permission is separate: tick only what you want. None of them is a condition for the interview, and none comes pre-ticked. You can withdraw any of them at any time, free of charge, through the same contact given in the data section.",
    "translation_accept": "I allow my speech to be transcribed and translated subtitles and texts of this episode (including the description) to be published in: {{locales}}.",
    "dub_generic_accept": "I allow a dubbed version of this episode with a generic synthetic voice (not my voice), speaking the translation of my words, disclosed to the audience as AI dubbing, in: {{locales}}.",
    "dub_replica_accept": "SENSITIVE DATA — I give specific, explicit consent to the creation of an artificial replica of my voice solely to dub THIS episode in {{locales}}, by the provider {{provider}} ({{country}}), with my voice model deleted within {{days}} days after dubbing. The dubbed version will be disclosed to the audience as AI-made. I can withdraw at any time.",
    "dub_replica_purpose": "dub this episode with an artificial replica of the data subject's voice"
  },
  "kit": {
    "title": "Guest kit",
    "greeting": "Hello, {{guest.preferred_name}}!",
    "thanks": "We are glad to have you on {{show.name}}. This kit gathers what you need to know before the recording. Read it calmly, whenever you can.",
    "about_heading": "What {{show.name}} is",
    "pillars_heading": "The topics we cover",
    "when_heading": "When",
    "when_tbd": "The date is still to be agreed with the production team.",
    "where_heading": "Where (in-person recording)",
    "address_label": "Address",
    "landmarks_label": "Landmarks",
    "gps_label": "In your GPS or ride app, type",
    "parking_label": "Parking",
    "arrive": "Please arrive {{arrive.min}} to {{arrive.max}} minutes early, to have some water and test the sound without rushing.",
    "remote_heading": "Remote recording: what you need",
    "remote_default": [
      "Headphones (wired, if you have them)",
      "A quiet room with little echo",
      "A stable connection; cable rather than Wi-Fi if possible",
      "Computer charged or plugged in"
    ],
    "conduct_heading": "So you can feel at ease",
    "conduct_default": [
      "There are no wrong answers: it is a conversation, not an exam.",
      "If you stumble or want to redo an answer, just say so. We edit.",
      "You can ask not to discuss a topic at any moment.",
      "Water whenever you like, and breaks too."
    ],
    "materials_heading": "Materials (optional)",
    "materials_text": "Want to send slides, PDFs, photos or links? Reply to this email with attachments. No account needed anywhere.",
    "privacy_heading": "Your data",
    "privacy_text": "We use your answers only to prepare this interview. To access, correct, delete or withdraw consent: {{controller.contact}}.",
    "signoff": "See you soon!",
    "parking": {
      "disponivel": "available on site",
      "indisponivel": "no parking on site",
      "pago_proximo": "paid parking nearby",
      "pendente": "to be confirmed by the production team"
    }
  },
  "messages": {
    "email_subject": "Guest kit · {{show.name}}",
    "owner_subject": "✅ {{guest.preferred_name}} filled in the form · {{show.name}}",
    "calendar_title": "{{show.name}} recording with {{guest.preferred_name}}",
    "calendar_remote_location": "Online (link from the production team)",
    "calendar_description": "Guest kit sent by email. Questions: {{controller.contact}}.",
    "whatsapp_kit": "Hello, {{guest.preferred_name}}! This is {{show.name}}. We got your form, thank you! The guest kit with all the details is in your email.{{#address_line}} Address: {{address_line}}.{{/address_line}}{{#gps_hint}} In your GPS, type: {{gps_hint}}.{{/gps_hint}}",
    "reminder_subject": "Tomorrow: recording at {{show.name}}",
    "reminder_body": "Hello, {{guest.preferred_name}}! Reminder: the {{show.name}} recording is tomorrow, {{scheduled_text}}.{{#address_line}} Address: {{address_line}}.{{/address_line}}{{#gps_hint}} In your GPS, type: {{gps_hint}}.{{/gps_hint}}{{#arrive}} Please arrive {{arrive.min}} to {{arrive.max}} minutes early.{{/arrive}} Any questions, just reply."
  },
  "invitation": {
    "subject": "Official invitation · {{show.name}}",
    "preheader": "{{show.name}} invites you to a conversation. Date, place and form inside.",
    "title": "Official invitation",
    "greeting": "Hello, {{guest.name}}!",
    "intro": {
      "formal": "We are honored to invite you to be a guest on {{show.name}}.",
      "cordial": "It is a pleasure to invite you for a conversation on {{show.name}}.",
      "descontraido": "Let's record? We'd love to have you on {{show.name}}."
    },
    "when_label": "Date and time",
    "when_tbd": "to be agreed with the production team",
    "where_label": "Place",
    "gps_label": "In your GPS or ride app, type",
    "arrival_label": "How to get there",
    "arrive": "Please arrive {{arrive.min}} to {{arrive.max}} minutes early.",
    "remote_label": "Remote recording, room link",
    "remote_link_tbd": "the room link will arrive by e-mail before the recording",
    "about_heading": "What {{show.name}} is",
    "cta_intro": {
      "essencial": "So we can prepare a conversation worthy of you, please fill in the guest form. It takes about 2 minutes.",
      "completo": "So we can prepare a conversation worthy of you, please fill in the guest form. It takes about 8 minutes, and almost everything is optional."
    },
    "cta_button": "Fill in the form",
    "cta_fallback": "If the button does not open, copy and paste this address into your browser:",
    "signoff": "Kind regards,",
    "footer_controller": "Sent by: {{controller.name}}, data controller. Contact: {{controller.contact}}.",
    "footer_purpose": "You received this invitation because {{signature.name}} suggested you as a guest. We use your name and e-mail only for this invitation and to organize the interview; the guest kit arrives after you answer the form.",
    "footer_optout": "Don't want to hear from {{show.name}} again? Reply to this e-mail with the word STOP and we will not send anything else.",
    "footer_brand": "Prepared with PodFácil",
    "ics_description": "Official invitation from {{show.name}}. Guest form: {{form_url}}"
  },
  "decision": {
    "ack": {
      "v1": "I have read the alerts above. I understand the plugin only recommends: the decision to go against the recommendation is mine, and the editorial and legal responsibility for what is recorded and published is mine (or of whom I represent), not the plugin's nor its authors'."
    },
    "alerts": {
      "R-CLAIM-CONDUTA-FONTES": "This statement about someone's conduct lacks the recommended backing (verified status with 1 primary source or 2 independent press sources). Using it on air may create defamation liability.",
      "R-CLAIM-CONDUTA-INDEPENDENCIA": "The press sources for this conduct statement may not be independent (same domain, author or agency). Check author, outlet and agency before deciding.",
      "R-ROTEIRO-GATE-PENDENTE": "The @guardian review (fact-check) has not been done yet for a mode that recommends it before recording.",
      "R-ROTEIRO-GATE-AJUSTES": "The @guardian recommended adjustments that are not recorded as applied.",
      "R-ROTEIRO-GATE-VETADO": "The @guardian recommended NOT recording this script as is. Recording against that recommendation is your decision and your responsibility.",
      "R-ROTEIRO-CONTRADITORIO": "This mode recommends hearing the named party before recording, and no right-of-reply request is recorded.",
      "R-ROTEIRO-REVISAO-JURIDICA": "This mode carries high legal risk and the recommended human legal review is still pending.",
      "R-ROTEIRO-SEM-LASTRO": "Some factual statements have no dossier claim nor source. Saying unbacked things on air is your editorial risk.",
      "R-ROTEIRO-INFERENCIA-COMO-FATO": "An inference (hypothesis) appears as a factual statement. The recommendation is to turn it into a question or hypothesis.",
      "R-ROTEIRO-RIGOR": "The mode asks for sources for numbers, dates and quotes, and this statement rests only on self-declared information.",
      "R-ROTEIRO-DEGRADADO": "The dossier is incomplete and this block uses its statements without a caveat to confirm with the guest.",
      "R-ROTEIRO-TIMING": "The sum of block durations is more than 15% away from the target duration.",
      "R-FACTCHECK-SEM-FONTE": "The fact-check found no source for this statement.",
      "R-FACTCHECK-DISCLOSURE": "The recommended advertising or sponsorship disclosure is missing.",
      "R-LOCALIZACAO-REVISAO-HUMANA": "Machine translation: review source and translation side by side (names, numbers, glossary terms) before publishing.",
      "R-LOCALIZACAO-SEM-ACEITE-TRADUCAO": "There is no recorded guest consent for translated subtitles and texts in this language. Publishing anyway is your decision and responsibility.",
      "R-LOCALIZACAO-SEM-ACEITE-VOZ-GENERICA": "There is no recorded guest consent for dubbing with a generic synthetic voice in this language. Publishing anyway is your decision and responsibility.",
      "R-LOCALIZACAO-AGENTE-POLITICO": "The guest is flagged as a candidate or political figure. Synthetic content with candidates' voices is subject to electoral rules in Brazil (TSE Resolution 23.732/2024; secondary source, check the current text): verify the electoral calendar and labelling before publishing the dub.",
      "R-LOCALIZACAO-GLOSSARIO": "Show glossary terms do not appear as expected in the translation (proper name, acronym or do-not-translate term).",
      "R-LOCALIZACAO-NUMEROS": "Some numbers from the source (dates, rates, statute articles) do not appear in the translation.",
      "R-LOCALIZACAO-CPS": "Some subtitles exceed the reading-speed limit (characters per second).",
      "R-FACTCHECK-LGPD": "Third-party personal data is cited without a clear legal basis. (Sensitive data not self-declared is not an alert: it is forbidden.)",
      "R-PUBLICACAO-GATE": "The episode quality gate did not recommend publication (REQUEST CHANGES or HOLD).",
      "R-MEMORIA-ROTEIRO-PENDENTE": "No script linked to this episode is ready to record (pronto_para_gravar). Recording anyway is your decision and responsibility."
    }
  },
  "localization": {
    "language_names": {
      "pt-BR": "Portuguese",
      "en": "English",
      "es": "Spanish",
      "zh": "Chinese"
    },
    "disclosure": {
      "subtitles": "Machine translation reviewed by {{show}}.",
      "dub_generic": "AI-dubbed version of the original {{source_language}} episode. Voices are synthetic.",
      "dub_replica": "AI-dubbed version of the original {{source_language}} episode, using authorized AI replicas of the speakers' voices."
    }
  },
  "owner": {
    "failed": {
      "subject": "PodFácil: a form answer was not processed",
      "body": "A guest form answer arrived on {{quando}}, but PodFácil could not process it.\n\nReason: {{motivo}}\n\nThe guest may not have received the kit or the calendar invitation. The answer is saved in the \"Form responses\" tab of your spreadsheet. Show this email to Claude in the chat to sort it out."
    },
    "confirm_hint": "To ask the guest for a correction: in the Guests tab, click their row and use PodFácil > Send confirmation.",
    "headline": "{{name}} filled in the form.",
    "lead": "Everything is recorded. Below is what has happened so far and what they told you.",
    "happened": "What has happened",
    "form_received": "Invitation received and form filled in",
    "attention": "Needs your attention",
    "summary": "Guest summary",
    "button": "See the full answers",
    "next_step": "Next step: ask Claude to \"prepare the briefing for {{name}}\" to get the dossier and the topic plan.",
    "notes": "Notes",
    "record_code": "Record code: {{id}}",
    "full_answers": "Full answers: {{url}}",
    "labels": {
      "name": "Name",
      "prefers": "prefers to be called {{name}}",
      "role": "Role",
      "bio": "Short bio",
      "ideas": "Key ideas",
      "recording": "Recording",
      "email": "Email",
      "whatsapp": "WhatsApp"
    },
    "mode": {
      "presencial": "In person",
      "remoto": "Remote"
    },
    "date_tbd": "to be agreed",
    "sends": {
      "kit_email": "Guest kit by email",
      "kit_whatsapp": "Guest kit by WhatsApp",
      "calendar": "Calendar invitation",
      "automations": "Automatic sends (kit and calendar)", "guest": "Send to the guest",
      "other": "Send \"{{key}}\""
    },
    "status": {
      "sent": "{{label}}: sent",
      "skipped": "{{label}}: not sent",
      "off": "{{label}}: WhatsApp is not set up in this spreadsheet",
      "error": "{{label}}: failed",
      "held": "{{label}}: waiting for your confirmation"
    },
    "drops": {
      "check.time_odd": "The time given ({{hora}}) is unusual. Check with the guest that it is not a typo.",
      "check.past": "The recording date given ({{data}}) has already passed. Confirm the date with the guest.",
      "check.whatsapp_mismatch": "The WhatsApp number given ends in {{agora}}, but the one noted in the invitation ends in {{antes}}. Confirm which one is right.",
      "whatsapp": "The WhatsApp number provided was not recognized{{end}}. Please confirm the number with the guest.",
      "whatsapp_end": " (ends in {{digits}})",
      "accessibility": "The guest wrote something about accessibility but did not tick the consent for this kind of data, so it was discarded. If it matters for the recording, ask them directly.",
      "sensitive": "A piece of sensitive personal data was discarded because the guest did not tick the specific consent.",
      "scheduled_at": "The recording date could not be read. Please confirm the date with the guest.",
      "previous_interviews": "The previous interviews field had an answer that was not a link; it was ignored.",
      "links": "One of the links was not a valid address and was ignored.",
      "key_ideas": "The guest sent more than 3 key ideas; the first 3 were kept.",
      "other": "An answer in the \"{{field}}\" field was ignored."
    },
    "held": "Answer without a valid invitation code: nothing was sent to the guest. If you invited them, confirm it from the menu or with confirmarIntake."
  },
  "sheet": {
    "tab": "Guests",
    "columns": [
      "Answered on",
      "Name",
      "Preferred name",
      "Role",
      "Short bio",
      "Key ideas",
      "Wants to promote",
      "Open to debate",
      "Prefers to avoid",
      "Recording",
      "Format",
      "Email",
      "WhatsApp",
      "Preferred contact",
      "Review before publishing",
      "What was sent",
      "Needs attention",
      "Briefing",
      "Record code"
    ],
    "not_informed": "not provided or not recognized",
    "none": "—",
    "briefing_link": "Open the briefing"
  },
  "menu": {
    "forget_yes": "Forget {{nome}}",
    "window": {
      "cancel": "Cancel",
      "not_now": "Not now",
      "continue": "Continue",
      "working": "Working…",
      "failed": "Something went wrong talking to Google. Close this window and try again.",
      "ok": "Close",
      "copy": "Copy",
      "copied": "Copied ✓",
      "open": "Open"
    },
    "start": {
      "guide": "Illustrated guide, screen by screen:",
      "tab": "Start here",
      "title": "Start here: from zero to the first invitation in about 15 minutes",
      "steps": [
        "This is your copy of the PodFácil spreadsheet. It is yours alone: nobody else sees what you put here.",
        "In the Claude chat, ask: \"set up my show in PodFácil\". Claude asks the questions and saves the show profile.",
        "Here in the spreadsheet, use the PodFácil menu (at the top, next to Help). Paid plan: PodFácil > Activate license. Free plan: PodFácil > Configure show and type the code Claude showed. If the menu does not appear, reload the page.",
        "The first time, Google asks for authorization and shows the screen \"Google hasn't verified this app\", with YOUR email as the developer. That is expected: the copy is yours and PodFácil runs inside your account. Click Advanced, then \"Go to PodFácil — planilha do programa (unsafe)\" and Continue; in the permissions list, leave everything ticked and click Continue. The window closes by itself and the option you chose usually carries on by itself; if nothing appears within a few seconds, click the menu option again.",
        "What Google asks for and what PodFácil does: Google asks for access to your spreadsheets, forms and calendars because it has no narrower permission for this, but PodFácil only touches this spreadsheet, the guest form and the recording events it creates; in Drive, only the files it creates itself. It also sends emails on your behalf (invitations and notices), checks your license on the PodFácil server and runs by itself once a day (reminders and the invitation queue). It does not read your emails.",
        "Once the show is configured, PodFácil creates the guest form. Then, in the Invitations tab, write one row per guest (name and email are enough) and use PodFácil > Invite.",
        "When a guest replies, a notice arrives in your email and the answer appears in the Guests tab."
      ],
      "footer": "Questions or something odd? Use PodFácil > Check installation or ask Claude in the chat."
    },
    "invite": "Invite (Invitations tab)",
    "confirm_guest": "Send confirmation to the selected guest",
    "invites": {
      "wait": "Checking the Invitations tab…",
      "send_button": "Send {{n}} invitation(s)",
      "wait_send": "Sending the invitations…",
      "busy": "The invitation queue is already running. Wait a few minutes and check the Status column.",
      "tab": "Invitations",
      "columns": [
        "Name",
        "Email",
        "Date and time",
        "Format",
        "Room link (remote)",
        "WhatsApp (optional)",
        "Status"
      ],
      "note": "One row per guest: name and email are enough; date, format, link and WhatsApp when you know them. Then use PodFácil > Invite. PodFácil fills in the Status column.",
      "created": "I created the {{aba}} tab. Fill in one row per guest (name and email are enough) and use PodFácil > Invite again.",
      "nothing": "No pending invitations in the {{aba}} tab. Rows with ✅ or ➖ are done: the same person never gets the invitation twice for the same date.",
      "confirm": "Send {{n}} invitation(s) now?",
      "done": "Done.",
      "done_lines": {
        "enviados": "✅ Invitations sent: {{n}}",
        "pulados": "➖ Already received (not resent): {{n}}",
        "corrigir": "❌ To fix (see the Status column): {{n}}",
        "falhas": "⚠️ Failed (use Invite again): {{n}}",
        "depois": "⏳ Left for later: {{n}}"
      },
      "later": "The ones left for later go out by themselves tomorrow, at the daily reminder time.",
      "need_form": "Before inviting, the show must be configured and the form created. Use PodFácil > Check installation.",
      "status": {
        "unsure": "⚠️ Not sure it was sent (the round was cut short): check Sent in Gmail; if it did not go out, use Invite again",
        "sent": "✅ Sent on {{quando}}",
        "sent_logo": "✅ Sent on {{quando}}, without the logo (use PodFácil > Upload logo)",
        "already": "➖ Already sent before",
        "optout": "➖ Not sent: this person asked not to receive emails",
        "quota": "⏳ Queued: today's email quota ran out; goes out tomorrow",
        "time": "⏳ Queued: goes out in the next round",
        "failed": "⚠️ Failed: {{motivo}}. Use Invite again to retry",
        "fix": "❌ Fix: {{motivo}}"
      },
      "errors": {
        "past": "the date has already passed",
        "name": "name is missing",
        "email": "invalid email",
        "date": "date and time not recognized (use 2026-10-20 14:30)",
        "mode": "format not recognized (use {{modos}})",
        "link": "the room link must start with https://",
        "whatsapp": "WhatsApp not recognized (use +country code and number)"
      },
      "digest_subject": "Invitation queue: {{enviados}} sent today",
      "digest_body": "The invitation queue ran by itself today. Sent: {{enviados}} · to fix: {{corrigir}} · failed: {{falhas}} · still queued: {{depois}}. See the {{aba}} tab: {{url}}"
    },
    "confirm": {
      "send_button": "Send the confirmation",
      "wait": "Sending…",
      "busy": "This confirmation is already going out; no need to click again.",
      "held": "This answer is on hold (it arrived without a valid invitation code). Confirm the guest before emailing them.",
      "title": "Send confirmation",
      "ask": "Send {{nome}} an email asking them to confirm {{n}} item(s)?\n\n{{itens}}",
      "ask_none": "I found nothing to fix in {{nome}}'s answers. Send an email asking them to confirm their details anyway?",
      "again": "A confirmation was already sent on {{quando}}.",
      "done": "Confirmation sent to {{nome}}. Their reply will arrive in your email.",
      "optout": "{{nome}} asked not to receive emails from the show; nothing was sent.",
      "quota": "Today's email quota ran out. Try again tomorrow.",
      "not_found": "I could not find this guest's answers (code {{id}})."
    },
    "title": "PodFácil",
    "activate_license": "Activate license",
    "check_install": "Check installation",
    "resend_notice": "Resend notice for the selected guest",
    "rebuild_guests": "Rebuild Guests tab",
    "forget_guest": "Forget selected guest (privacy)",
    "release_devices": "Free other devices",
    "ask_code_title": "Which guest?",
    "ask_code": "In the Guests tab, click the guest's row and choose the option again. Or paste the record code here (last column):",
    "resend_done": "Notice resent to your email.",
    "rebuild_done": "Guests tab rebuilt, briefing links kept.",
    "forget_confirm": "Forget {{nome}}? This deletes the answers, the Guests row and the calendar event, and moves the briefing to the trash. It cannot be undone.",
    "forget_done": "Done: {{nome}} was forgotten.",
    "forget_pending": "Still to do by hand:",
    "error": "That didn't work: {{motivo}}",
    "license": {
      "plans": {
        "free": "Free",
        "individual_solo": "Individual Solo",
        "individual_duo": "Individual Duo",
        "enterprise_10": "Studio, up to 10 people",
        "enterprise_20": "Studio, up to 20 people"
      },
      "upgrade_hint": "Your license unlocks the complete form: to replace the essential one, use Check installation.",
      "ok_stay": "License activated ({{plano}} plan). Copy what you need above and close this window.",
      "ok_read": "License activated ({{plano}} plan). Read the note below and close this window.",
      "title": "Activate your PodFácil license",
      "lead": "Paste the key you received by email after your purchase. It is stored only in this project and never shown on screen.",
      "label": "License key",
      "button": "Activate",
      "working": "Checking with the server…",
      "ok": "License activated ({{plano}} plan). This window closes by itself.",
      "saved_offline": "Key saved. The PodFácil server did not answer just now; it will be checked on next use.",
      "invalid": "That doesn't look like a license key. The key starts with pgi_ and has 47 letters, digits, - and _. In the email, don't double-click (it stops at the first hyphen): select by dragging from the start to the end of the key, copy and paste it here.",
      "refused": "The server refused the key: {{motivo}}",
      "free_key": "That key is on the free plan. Automations are part of the paid plan.",
      "saved_limit": "Key saved. It has reached its computer limit: use PodFácil > Free other devices.",
      "offline_keep": "The PodFácil server did not answer just now and a key is already saved; it stays in use. Try changing it again in a few minutes.",
      "unknown": "The server does not recognize this key. Check that you copied the whole key from the email.",
      "failed": "Something went wrong talking to Google. Close this window and try again."
    },
    "check": {
      "wait": "Checking the installation…",
      "form_ask_yes": "Create the form",
      "form_gone_yes": "Create a new one",
      "upgrade_yes": "Switch to complete",
      "form_gone_ask": "The saved form does not open (deleted or no access). Create a new one now? The guest link changes; answers already received stay in the spreadsheet.",
      "upgrade_ask": "Your paid license unlocks the complete form. Switch now? The guest link changes: the old one stops accepting answers, and answers already received stay in the spreadsheet.",
      "form_ask": "There is no guest form yet. Create it now? (takes a few seconds)",
      "phone_ok": "WhatsApp field in the form is validated (incomplete numbers or numbers with letters are rejected)",
      "title": "Check installation",
      "summary_ok": "PodFácil is all set.",
      "summary_fail": "{{n}} item(s) need you:",
      "show_ok": "Show settings: {{nome}}.",
      "show_missing": "The show settings are missing (Claude prepares them with you).",
      "form_ok": "Guest form found.",
      "form_missing": "The form has not been created yet.",
      "form_gone": "The saved form does not open (deleted or no access).",
      "triggers_ok": "Automatic sends are on.",
      "triggers_fixed": "Automatic sends were off and have been turned back on.",
      "guests_ok": "Guests tab in place.",
      "guests_fixed": "The Guests tab was missing and has been created.",
      "guests_fail": "Could not create the Guests tab: {{motivo}}",
      "license_none": "No license: free plan. For the paid plan, use PodFácil > Activate license.",
      "license_paid": "License active ({{plano}} plan).",
      "license_offline": "License saved; the server did not answer just now.",
      "license_fail": "License problem: {{motivo}}",
      "triggers_other": "Automatic sends were turned on by the account {{dono}}. Ask that person to open PodFácil > Check installation.",
      "logo_fail": "PodFácil cannot open the Drive logo; invitations go out with the show name instead. Upload it again via PodFácil > Upload logo.",
      "logo_ok": "Invitation logo in place."
    },
    "devices": {
      "confirm_yes": "Release the devices",
      "title": "Free other devices",
      "confirm": "This disconnects every computer linked to your license; each one works again on its next use. Allowed twice a month. Continue?",
      "done": "Devices freed.",
      "no_key": "Activate the license first (PodFácil > Activate license)."
    },
    "config": {
      "tz_label": "Time zone for dates",
      "ask_code_button": "Set up",
      "wait_profile": "Fetching the show profile…",
      "wait_form": "Creating the guest form in Google Forms. It takes 1 to 2 minutes: you can leave this window open.",
      "form_link": "Guest form link",
      "form_busy": "The form is already being created in another window. Wait a minute and use Check installation.",
      "form_exists": "The guest form already exists. Link for the guest: {{url}}",
      "form_created": "Guest form created ({{variante}}). Link for the guest: {{url}} The link is also kept in the Configuration tab.",
      "form_fail": "I could not create the form: {{motivo}}",
      "variants": {"essencial": "essential", "completo": "complete"},
      "item": "Configure show",
      "ask_code_title": "Show code",
      "ask_code": "Type the 15-character code (letters and numbers) Claude showed in the chat (with or without the dashes):",
      "done": "Show \"{{nome}}\" configured. The details are in the {{aba}} tab.",
      "tab": "Settings",
      "note": "This tab only shows the settings. To change them, ask Claude in the chat and use PodFácil > Configure show again.",
      "labels": {
        "name": "Show",
        "tagline": "Tagline",
        "locale": "Language",
        "editorial": "Editorial line",
        "modes": "Records",
        "studio": "Studio",
        "address": "Address",
        "colors": "Colors",
        "logo": "Logo",
        "controller": "Data controller",
        "retention": "Answers kept"
      },
      "retention_days": "{{dias}} days after publishing",
      "imported": "Show profile \"{{nome}}\" imported.",
      "logo_item": "Upload logo",
      "import_failed": "The show profile arrived, but it could not be saved ({{motivo}}). Ask Claude to save it again and use PodFácil > Configure show.",
      "logo": {
        "title": "Invitation logo",
        "lead": "Choose the show logo (PNG or JPG, up to 1 MB). It is embedded in invitations and kept in your Google Drive.",
        "button": "Upload",
        "working": "Uploading…",
        "ok": "Logo saved. The next invitations already include it.",
        "too_big": "The file is larger than 1 MB. Make the image smaller and try again.",
        "bad_type": "Use a PNG or JPG file.",
        "need_show": "Configure the show first (PodFácil > Configure show).",
        "failed": "Something went wrong uploading the logo. Try again."
      }
    }
  },
  "guest_confirm": {
    "subject": "{{show}}: could you confirm a few details about your appearance?",
    "greeting": "Hi {{nome}},",
    "intro": "Thank you for filling in the {{show}} form. Before the recording, we would like to confirm a few things:",
    "intro_none": "Thank you for filling in the {{show}} form. Before the recording, we would like to confirm the details below.",
    "items": {
      "contacts.whatsapp": "We could not read the WhatsApp number you gave{{end}}. What is the right number, with country code?",
      "accessibility": "You wrote something about accessibility but did not tick the authorization for us to keep this kind of information, so it was not recorded. If you would like us to prepare, reply to this email and we will work out how.",
      "scheduled_at": "We could not read the recording date and time. When works for you?",
      "check.time_odd": "The time you gave was {{hora}}. Is that right?",
      "check.past": "The date you gave ({{data}}) has already passed. What is the right date?",
      "check.whatsapp_mismatch": "The WhatsApp number you gave ends in {{agora}}, but we had noted one ending in {{antes}}. Which should we use?"
    },
    "end": " (ending in {{digits}})",
    "summary": "What we have on file",
    "labels": {
      "recording": "Recording",
      "whatsapp": "WhatsApp"
    },
    "whatsapp_end": "ends in {{digits}}",
    "closing": "Just reply to this email with the correction. If everything is right, reply \"all good\".",
    "signature": "The {{show}} team"
  }
}

```


## es.json

```json
{
  "locale": "es",
  "needs_native_review": true,
  "text_version": "es/v0-skeleton",
  "form": {
    "validation": {
      "phone": "Escribe el número con código de país y de área, ej.: +34 612 345 678."
    },
    "title": "[TODO-es] Guest of {{show.name}}",
    "description_essencial": "[TODO-es] Takes about 2 minutes. It helps us prepare a good conversation for you, with no surprises.",
    "description_completo": "[TODO-es] Takes about 8 minutes. Almost everything is optional: skip whatever you prefer.",
    "confirmation": "[TODO-es] Thank you! If you allowed email, the guest kit is on its way. To send files (PDFs, slides, photos), just reply to that email with attachments.",
    "sections": {
      "about": "[TODO-es] About you",
      "content": "[TODO-es] The conversation",
      "logistics": "[TODO-es] Recording",
      "channels": "[TODO-es] How we reach you",
      "consent": "[TODO-es] Your data and this interview",
      "sensitive": "[TODO-es] Sensitive data (optional)",
      "localization": "[TODO-es] Other languages (optional)"
    },
    "fields": {
      "guest.full_name": {
        "title": "[TODO-es] Full name",
        "help": ""
      },
      "guest.preferred_name": {
        "title": "[TODO-es] What should we call you on air?",
        "help": "[TODO-es] E.g. Ana, Dr. Ana, Professor Silva."
      },
      "guest.name_pronunciation": {
        "title": "[TODO-es] How is your name pronounced?",
        "help": "[TODO-es] Only if we might get it wrong."
      },
      "guest.pronouns": {
        "title": "[TODO-es] Pronouns",
        "help": "[TODO-es] Optional. E.g. she/her."
      },
      "guest.role_title": {
        "title": "[TODO-es] Role or occupation",
        "help": ""
      },
      "guest.photo_url": {
        "title": "[TODO-es] Link to a photo of you for promotion",
        "help": "[TODO-es] Optional. A public link (website, LinkedIn, shared Drive)."
      },
      "bio.short": {
        "title": "[TODO-es] Short bio, up to 2 lines",
        "help": "[TODO-es] This is what we read in the intro."
      },
      "bio.long": {
        "title": "[TODO-es] Full bio",
        "help": "[TODO-es] Optional."
      },
      "links": {
        "title": "[TODO-es] Your main links",
        "help": "[TODO-es] Website, profiles, portfolio. One per line. If you have none, leave it blank."
      },
      "social_handles": {
        "title": "[TODO-es] Handles to tag when we promote",
        "help": "[TODO-es] One per line, as network: @user (e.g. instagram: @ana)."
      },
      "previous_interviews": {
        "title": "[TODO-es] Interviews you have given",
        "help": "[TODO-es] Links, one per line. Helps us avoid repeating questions."
      },
      "key_ideas": {
        "title": "[TODO-es] Up to 3 ideas you want the audience to take away",
        "help": "[TODO-es] One per line."
      },
      "stories_to_tell": {
        "title": "[TODO-es] Stories you like to tell",
        "help": "[TODO-es] One per line."
      },
      "controversies.accepts": {
        "title": "[TODO-es] Controversial topics you are happy to discuss",
        "help": "[TODO-es] One per line."
      },
      "controversies.declines": {
        "title": "[TODO-es] Controversial topics you would rather avoid",
        "help": "[TODO-es] One per line."
      },
      "off_limits_topics": {
        "title": "[TODO-es] Off-limits topics",
        "help": "[TODO-es] We will not touch these. One per line."
      },
      "wants_to_promote": {
        "title": "[TODO-es] Anything you want to promote?",
        "help": "[TODO-es] Book, course, event, project. One per line."
      },
      "dream_questions": {
        "title": "[TODO-es] Questions you would love to be asked",
        "help": "[TODO-es] One per line."
      },
      "conflicts_of_interest.details": {
        "title": "[TODO-es] Conflicts of interest or sponsorships related to the topics",
        "help": "[TODO-es] Leave blank if none."
      },
      "companion.name": {
        "title": "[TODO-es] Bringing someone along? Who?",
        "help": "[TODO-es] Leave blank if coming alone."
      },
      "materials": {
        "title": "[TODO-es] Supporting materials (links)",
        "help": "[TODO-es] Talks, books, articles, videos. One link per line. Files: reply to the kit email with attachments."
      },
      "recording_mode": {
        "title": "[TODO-es] How will we record?",
        "help": ""
      },
      "scheduled_at": {
        "title": "[TODO-es] Date and time already agreed with us",
        "help": "[TODO-es] Only if already agreed. Used for the calendar invite and the day-before reminder."
      },
      "wants_prepublication_review": {
        "title": "[TODO-es] Would you like to see the episode before we publish?",
        "help": ""
      },
      "preferred_channel": {
        "title": "[TODO-es] Preferred channel to reach you",
        "help": ""
      },
      "contacts.email": {
        "title": "[TODO-es] Your email",
        "help": ""
      },
      "invite.token": {
        "title": "Código de invitación",
        "help": "Viene completado por el enlace de la invitación que recibiste por correo. No lo cambies. Si está vacío, envía igual: el programa lo confirmará contigo antes de enviar nada."
      },
      "contacts.whatsapp": {
        "title": "[TODO-es] Your WhatsApp",
        "help": "[TODO-es] Optional. With country code, e.g. +44 7700 900123."
      },
      "automation_consents": {
        "title": "[TODO-es] May we use these channels to send you the kit and reminders?",
        "help": "[TODO-es] Tick only what you want. Nothing ticked = nothing sent through that channel."
      },
      "image_voice": {
        "title": "[TODO-es] Image and voice",
        "help": ""
      },
      "consent.general": {
        "title": "[TODO-es] Consent",
        "help": ""
      },
      "consent.public_research": {
        "title": "[TODO-es] Research in public sources",
        "help": ""
      },
      "consent.divulgacao": {
        "title": "[TODO-es] Promotion (optional)",
        "help": ""
      },
      "accessibility.needs": {
        "title": "[TODO-es] SENSITIVE DATA — Do you need any accessibility accommodation?",
        "help": "[TODO-es] Optional. It may reveal health information: it is only used if you tick the consent right below."
      },
      "accessibility.accept": {
        "title": "[TODO-es] SENSITIVE DATA — Specific consent (accessibility)",
        "help": ""
      },
      "sensitive.category": {
        "title": "[TODO-es] SENSITIVE DATA — What is it about?",
        "help": "[TODO-es] Optional."
      },
      "sensitive.value": {
        "title": "[TODO-es] SENSITIVE DATA — What you want us to know",
        "help": "[TODO-es] Optional. Write only what you want in the preparation."
      },
      "sensitive.accept": {
        "title": "[TODO-es] SENSITIVE DATA — Specific consent",
        "help": ""
      },
      "localization.translation_text": {
        "title": "[TODO-es] Translated subtitles and texts",
        "help": ""
      },
      "localization.dub_generic_voice": {
        "title": "[TODO-es] Dubbing with a generic synthetic voice",
        "help": ""
      },
      "localization.dub_voice_replica": {
        "title": "[TODO-es] SENSITIVE DATA — Artificial replica of your voice",
        "help": ""
      }
    },
    "choices": {
      "recording_mode": {
        "presencial": "[TODO-es] In person, at the studio",
        "remoto": "[TODO-es] Remote, online"
      },
      "yes_no": {
        "yes": "[TODO-es] Yes",
        "no": "[TODO-es] No"
      },
      "preferred_channel": {
        "email": "[TODO-es] Email",
        "whatsapp": "[TODO-es] WhatsApp",
        "phone": "[TODO-es] Phone",
        "other": "[TODO-es] Other"
      },
      "channels": {
        "email": "[TODO-es] Email: guest kit and a day-before reminder",
        "whatsapp": "[TODO-es] WhatsApp: kit and a day-before reminder",
        "calendar": "[TODO-es] Calendar: invite with date and address"
      },
      "sensitive_category": {
        "origem_racial_etnica": "[TODO-es] Racial or ethnic origin",
        "conviccao_religiosa": "[TODO-es] Religious belief",
        "opiniao_politica": "[TODO-es] Political opinion",
        "filiacao_sindical_religiosa_filosofica_politica": "[TODO-es] Trade union or religious, philosophical or political membership",
        "saude": "[TODO-es] Health",
        "vida_sexual": "[TODO-es] Sex life",
        "genetico": "[TODO-es] Genetic data",
        "biometrico": "[TODO-es] Biometric data"
      }
    }
  },
  "consent": {
    "contact_email": "[TODO-es] by email at {{email}}",
    "contact_reply_to_email": "[TODO-es] by replying to any email from this show (including the invitation or the guest kit)",
    "clauses": {
      "BR-LGPD": {
        "clause_id": "BR-LGPD/v1",
        "legal_review": "pending",
        "text": "[TODO-es] {{controller.name}} (data controller{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contact: {{controller.contact}}) will use the answers to this form only for the purposes below, related to your interview on {{show.name}}: {{purposes}}.\n\nTo prepare better questions, we will also look at information you have made public yourself (website, social media, interviews and published texts). Everything that goes into the preparation material will cite its source.\n\nWe will not use or keep sensitive data (health, religion, political opinion, sex life, racial or ethnic origin, among others) unless you write it yourself in the optional sensitive-data section and tick the specific consent for each item. It is your decision.\n\nThe data is deleted within {{retention_days}} days after the episode is published; we keep only the record of this consent, as proof. At any time and free of charge you may request access, correction or deletion, or withdraw this consent, {{controller.contact}}. If you do not want to consent, simply do not submit the form: the interview can still happen without it."
      },
      "EU-GDPR": {
        "clause_id": "EU-GDPR/v1",
        "legal_review": "pending",
        "text": "[TODO-es] {{controller.name}} (data controller{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contact: {{controller.contact}}) will process the answers to this form based on your consent, only for: {{purposes}}.\n\nWe will also look at information you have made publicly accessible (website, social media, interviews, published texts), always citing the source.\n\nSpecial categories of data (health, religion, political opinion, sex life, racial or ethnic origin, among others) are processed only if you write them in the optional section and give explicit consent for each item.\n\nThe data is deleted within {{retention_days}} days after the episode is published. You have the right of access, rectification, erasure, restriction, portability and objection, and you may withdraw consent at any time ({{controller.contact}}) without affecting processing already carried out. You may also lodge a complaint with a supervisory authority."
      },
      "other": {
        "clause_id": "other/v1",
        "legal_review": "pending",
        "text": "[TODO-es] {{controller.name}} (contact: {{controller.contact}}) will use the answers to this form only for: {{purposes}}. We will also look at information you have made public, always citing the source. Sensitive data is used only if you write it in the optional section and tick the specific consent. The data is deleted within {{retention_days}} days after publication. To access, correct, delete or withdraw consent: {{controller.contact}}."
      }
    },
    "purposes": {
      "preparo_entrevista": "[TODO-es] preparing your interview",
      "dossie": "[TODO-es] building the preparation material (with sources)",
      "memoria_episodio": "[TODO-es] recording the episode in the show's archive",
      "divulgacao": "[TODO-es] promoting the episode with your short bio, photo and handle"
    },
    "draft_notice": "[TODO-es] NOTICE: this consent text is a DRAFT (v0) under legal review and may change. If the final version changes anything, we will ask for your consent again.",
    "general_accept": "[TODO-es] I have read the text above and agree to the use of my answers for these purposes.",
    "public_research_accept": "[TODO-es] I understand that information I have made public myself will be consulted, always citing the source.",
    "divulgacao_accept": "[TODO-es] I also allow my short bio, photo and handle to be used to promote the episode.",
    "image_voice_accept": "[TODO-es] I authorise the recording and publication of my image and voice in this episode.",
    "sensitive_intro": "[TODO-es] This section is entirely optional and the decision is yours. Everything here is SENSITIVE DATA: it is used only if you write it and tick the specific consent right below each field. Without consent the information is discarded and not kept.",
    "sensitive_accept": "[TODO-es] SENSITIVE DATA — I give specific, explicit consent to the use of the information I wrote above only to prepare and conduct this interview.",
    "accessibility_accept": "[TODO-es] SENSITIVE DATA (may reveal health) — I allow the accessibility need above to be used only to organise the recording logistics.",
    "sensitive_purpose": "[TODO-es] prepare and conduct this interview",
    "accessibility_purpose": "[TODO-es] organise the recording logistics",
    "localization_intro": "[TODO-es] This section is optional and each permission is separate: tick only what you want. None of them is a condition for the interview, and none comes pre-ticked. You can withdraw any of them at any time, free of charge, through the same contact given in the data section.",
    "translation_accept": "[TODO-es] I allow my speech to be transcribed and translated subtitles and texts of this episode (including the description) to be published in: {{locales}}.",
    "dub_generic_accept": "[TODO-es] I allow a dubbed version of this episode with a generic synthetic voice (not my voice), speaking the translation of my words, disclosed to the audience as AI dubbing, in: {{locales}}.",
    "dub_replica_accept": "[TODO-es] SENSITIVE DATA — I give specific, explicit consent to the creation of an artificial replica of my voice solely to dub THIS episode in {{locales}}, by the provider {{provider}} ({{country}}), with my voice model deleted within {{days}} days after dubbing. The dubbed version will be disclosed to the audience as AI-made. I can withdraw at any time.",
    "dub_replica_purpose": "[TODO-es] dub this episode with an artificial replica of the data subject's voice"
  },
  "kit": {
    "title": "[TODO-es] Guest kit",
    "greeting": "[TODO-es] Hello, {{guest.preferred_name}}!",
    "thanks": "[TODO-es] We are glad to have you on {{show.name}}. This kit gathers what you need to know before the recording. Read it calmly, whenever you can.",
    "about_heading": "[TODO-es] What {{show.name}} is",
    "pillars_heading": "[TODO-es] The topics we cover",
    "when_heading": "[TODO-es] When",
    "when_tbd": "[TODO-es] The date is still to be agreed with the production team.",
    "where_heading": "[TODO-es] Where (in-person recording)",
    "address_label": "[TODO-es] Address",
    "landmarks_label": "[TODO-es] Landmarks",
    "gps_label": "[TODO-es] In your GPS or ride app, type",
    "parking_label": "[TODO-es] Parking",
    "arrive": "[TODO-es] Please arrive {{arrive.min}} to {{arrive.max}} minutes early, to have some water and test the sound without rushing.",
    "remote_heading": "[TODO-es] Remote recording: what you need",
    "remote_default": [
      "[TODO-es] Headphones (wired, if you have them)",
      "[TODO-es] A quiet room with little echo",
      "[TODO-es] A stable connection; cable rather than Wi-Fi if possible",
      "[TODO-es] Computer charged or plugged in"
    ],
    "conduct_heading": "[TODO-es] So you can feel at ease",
    "conduct_default": [
      "[TODO-es] There are no wrong answers: it is a conversation, not an exam.",
      "[TODO-es] If you stumble or want to redo an answer, just say so. We edit.",
      "[TODO-es] You can ask not to discuss a topic at any moment.",
      "[TODO-es] Water whenever you like, and breaks too."
    ],
    "materials_heading": "[TODO-es] Materials (optional)",
    "materials_text": "[TODO-es] Want to send slides, PDFs, photos or links? Reply to this email with attachments. No account needed anywhere.",
    "privacy_heading": "[TODO-es] Your data",
    "privacy_text": "[TODO-es] We use your answers only to prepare this interview. To access, correct, delete or withdraw consent: {{controller.contact}}.",
    "signoff": "[TODO-es] See you soon!",
    "parking": {
      "disponivel": "[TODO-es] available on site",
      "indisponivel": "[TODO-es] no parking on site",
      "pago_proximo": "[TODO-es] paid parking nearby",
      "pendente": "[TODO-es] to be confirmed by the production team"
    }
  },
  "messages": {
    "email_subject": "[TODO-es] Guest kit · {{show.name}}",
    "owner_subject": "✅ {{guest.preferred_name}} respondió el formulario · {{show.name}}",
    "calendar_title": "[TODO-es] {{show.name}} recording with {{guest.preferred_name}}",
    "calendar_remote_location": "[TODO-es] Online (link from the production team)",
    "calendar_description": "[TODO-es] Guest kit sent by email. Questions: {{controller.contact}}.",
    "whatsapp_kit": "[TODO-es] Hello, {{guest.preferred_name}}! This is {{show.name}}. We got your form, thank you! The guest kit with all the details is in your email.{{#address_line}} Address: {{address_line}}.{{/address_line}}{{#gps_hint}} In your GPS, type: {{gps_hint}}.{{/gps_hint}}",
    "reminder_subject": "[TODO-es] Tomorrow: recording at {{show.name}}",
    "reminder_body": "[TODO-es] Hello, {{guest.preferred_name}}! Reminder: the {{show.name}} recording is tomorrow, {{scheduled_text}}.{{#address_line}} Address: {{address_line}}.{{/address_line}}{{#gps_hint}} In your GPS, type: {{gps_hint}}.{{/gps_hint}}{{#arrive}} Please arrive {{arrive.min}} to {{arrive.max}} minutes early.{{/arrive}} Any questions, just reply."
  },
  "_note": "ESQUELETO: textos copiados do en e marcados [TODO-es]. Precisa de tradução e revisão nativa (e jurídica) antes de uso. O build do formulário recusa este locale enquanto needs_native_review=true, salvo ALLOW_UNREVIEWED_LOCALE=true.",
  "invitation": {
    "subject": "[TODO-es] Official invitation · {{show.name}}",
    "preheader": "[TODO-es] {{show.name}} invites you to a conversation. Date, place and form inside.",
    "title": "[TODO-es] Official invitation",
    "greeting": "[TODO-es] Hello, {{guest.name}}!",
    "intro": {
      "formal": "[TODO-es] We are honored to invite you to be a guest on {{show.name}}.",
      "cordial": "[TODO-es] It is a pleasure to invite you for a conversation on {{show.name}}.",
      "descontraido": "[TODO-es] Let's record? We'd love to have you on {{show.name}}."
    },
    "when_label": "[TODO-es] Date and time",
    "when_tbd": "[TODO-es] to be agreed with the production team",
    "where_label": "[TODO-es] Place",
    "gps_label": "[TODO-es] In your GPS or ride app, type",
    "arrival_label": "[TODO-es] How to get there",
    "arrive": "[TODO-es] Please arrive {{arrive.min}} to {{arrive.max}} minutes early.",
    "remote_label": "[TODO-es] Remote recording, room link",
    "remote_link_tbd": "[TODO-es] the room link will arrive by e-mail before the recording",
    "about_heading": "[TODO-es] What {{show.name}} is",
    "cta_intro": {
      "essencial": "[TODO-es] So we can prepare a conversation worthy of you, please fill in the guest form. It takes about 2 minutes.",
      "completo": "[TODO-es] So we can prepare a conversation worthy of you, please fill in the guest form. It takes about 8 minutes, and almost everything is optional."
    },
    "cta_button": "[TODO-es] Fill in the form",
    "cta_fallback": "[TODO-es] If the button does not open, copy and paste this address into your browser:",
    "signoff": "[TODO-es] Kind regards,",
    "footer_controller": "[TODO-es] Sent by: {{controller.name}}, data controller. Contact: {{controller.contact}}.",
    "footer_purpose": "[TODO-es] You received this invitation because {{signature.name}} suggested you as a guest. We use your name and e-mail only for this invitation and to organize the interview; the guest kit arrives after you answer the form.",
    "footer_optout": "[TODO-es] Don't want to hear from {{show.name}} again? Reply to this e-mail with the word STOP and we will not send anything else.",
    "footer_brand": "[TODO-es] Prepared with PodFácil",
    "ics_description": "[TODO-es] Official invitation from {{show.name}}. Guest form: {{form_url}}"
  },
  "decision": {
    "ack": {
      "v1": "[TODO-es] I have read the alerts above. I understand the plugin only recommends: the decision to go against the recommendation is mine, and the editorial and legal responsibility for what is recorded and published is mine (or of whom I represent), not the plugin's nor its authors'."
    },
    "alerts": {
      "R-CLAIM-CONDUTA-FONTES": "[TODO-es] This statement about someone's conduct lacks the recommended backing (verified status with 1 primary source or 2 independent press sources). Using it on air may create defamation liability.",
      "R-CLAIM-CONDUTA-INDEPENDENCIA": "[TODO-es] The press sources for this conduct statement may not be independent (same domain, author or agency). Check author, outlet and agency before deciding.",
      "R-ROTEIRO-GATE-PENDENTE": "[TODO-es] The @guardian review (fact-check) has not been done yet for a mode that recommends it before recording.",
      "R-ROTEIRO-GATE-AJUSTES": "[TODO-es] The @guardian recommended adjustments that are not recorded as applied.",
      "R-ROTEIRO-GATE-VETADO": "[TODO-es] The @guardian recommended NOT recording this script as is. Recording against that recommendation is your decision and your responsibility.",
      "R-ROTEIRO-CONTRADITORIO": "[TODO-es] This mode recommends hearing the named party before recording, and no right-of-reply request is recorded.",
      "R-ROTEIRO-REVISAO-JURIDICA": "[TODO-es] This mode carries high legal risk and the recommended human legal review is still pending.",
      "R-ROTEIRO-SEM-LASTRO": "[TODO-es] Some factual statements have no dossier claim nor source. Saying unbacked things on air is your editorial risk.",
      "R-ROTEIRO-INFERENCIA-COMO-FATO": "[TODO-es] An inference (hypothesis) appears as a factual statement. The recommendation is to turn it into a question or hypothesis.",
      "R-ROTEIRO-RIGOR": "[TODO-es] The mode asks for sources for numbers, dates and quotes, and this statement rests only on self-declared information.",
      "R-ROTEIRO-DEGRADADO": "[TODO-es] The dossier is incomplete and this block uses its statements without a caveat to confirm with the guest.",
      "R-ROTEIRO-TIMING": "[TODO-es] The sum of block durations is more than 15% away from the target duration.",
      "R-FACTCHECK-SEM-FONTE": "[TODO-es] The fact-check found no source for this statement.",
      "R-FACTCHECK-DISCLOSURE": "[TODO-es] The recommended advertising or sponsorship disclosure is missing.",
      "R-FACTCHECK-LGPD": "[TODO-es] Third-party personal data is cited without a clear legal basis. (Sensitive data not self-declared is not an alert: it is forbidden.)",
      "R-PUBLICACAO-GATE": "[TODO-es] The episode quality gate did not recommend publication (REQUEST CHANGES or HOLD).",
      "R-MEMORIA-ROTEIRO-PENDENTE": "[TODO-es] No script linked to this episode is ready to record (pronto_para_gravar). Recording anyway is your decision and responsibility.",
      "R-LOCALIZACAO-REVISAO-HUMANA": "[TODO-es] Machine translation: review source and translation side by side (names, numbers, glossary terms) before publishing.",
      "R-LOCALIZACAO-SEM-ACEITE-TRADUCAO": "[TODO-es] There is no recorded guest consent for translated subtitles and texts in this language. Publishing anyway is your decision and responsibility.",
      "R-LOCALIZACAO-SEM-ACEITE-VOZ-GENERICA": "[TODO-es] There is no recorded guest consent for dubbing with a generic synthetic voice in this language. Publishing anyway is your decision and responsibility.",
      "R-LOCALIZACAO-AGENTE-POLITICO": "[TODO-es] The guest is flagged as a candidate or political figure. Synthetic content with candidates' voices is subject to electoral rules in Brazil (TSE Resolution 23.732/2024; secondary source, check the current text): verify the electoral calendar and labelling before publishing the dub.",
      "R-LOCALIZACAO-GLOSSARIO": "[TODO-es] Show glossary terms do not appear as expected in the translation (proper name, acronym or do-not-translate term).",
      "R-LOCALIZACAO-NUMEROS": "[TODO-es] Some numbers from the source (dates, rates, statute articles) do not appear in the translation.",
      "R-LOCALIZACAO-CPS": "[TODO-es] Some subtitles exceed the reading-speed limit (characters per second)."
    }
  },
  "localization": {
    "language_names": {
      "pt-BR": "portugués",
      "en": "inglés",
      "es": "español",
      "zh": "chino"
    },
    "disclosure": {
      "subtitles": "[TODO-es] Machine translation reviewed by {{show}}.",
      "dub_generic": "Versión doblada con inteligencia artificial a partir del episodio original en {{source_language}}. Las voces son sintéticas.",
      "dub_replica": "Versión doblada con inteligencia artificial, con réplicas autorizadas de las voces de los participantes, a partir del episodio original en {{source_language}}."
    }
  },
  "owner": {
    "failed": {
      "subject": "PodFácil: una respuesta del formulario no se procesó",
      "body": "Llegó una respuesta al formulario del invitado el {{quando}}, pero PodFácil no pudo procesarla.\n\nMotivo: {{motivo}}\n\nEs posible que el invitado no haya recibido el kit ni la invitación de la agenda. La respuesta está guardada en la pestaña \"Respuestas de formulario\" de tu hoja. Muestra este correo a Claude en el chat para resolverlo."
    },
    "confirm_hint": "Para pedir la corrección al invitado: en la pestaña Invitados, haz clic en su fila y usa PodFácil > Enviar confirmación.",
    "headline": "{{name}} respondió el formulario.",
    "lead": "Todo quedó registrado. Abajo ves lo que ya ocurrió y lo que la persona contó.",
    "happened": "Lo que ya ocurrió",
    "form_received": "Invitación recibida y formulario completado",
    "attention": "Necesita tu atención",
    "summary": "Resumen del invitado",
    "button": "Ver las respuestas completas",
    "next_step": "Siguiente paso: pide a Claude \"preparar el briefing de {{name}}\" para recibir el dosier y la pauta.",
    "notes": "Observaciones",
    "record_code": "Código del registro: {{id}}",
    "full_answers": "Respuestas completas: {{url}}",
    "labels": {
      "name": "Nombre",
      "prefers": "prefiere que le llamen {{name}}",
      "role": "Cargo / actividad",
      "bio": "Presentación",
      "ideas": "Ideas principales",
      "recording": "Grabación",
      "email": "Correo",
      "whatsapp": "WhatsApp"
    },
    "mode": {
      "presencial": "Presencial",
      "remoto": "Remota"
    },
    "date_tbd": "por definir",
    "sends": {
      "kit_email": "Kit del invitado por correo",
      "kit_whatsapp": "Kit del invitado por WhatsApp",
      "calendar": "Invitación en la agenda",
      "automations": "Envíos automáticos (kit y agenda)", "guest": "Envío al invitado",
      "other": "Envío \"{{key}}\""
    },
    "status": {
      "sent": "{{label}}: enviado",
      "skipped": "{{label}}: no enviado",
      "off": "{{label}}: WhatsApp no está activado en esta hoja",
      "error": "{{label}}: falló",
      "held": "{{label}}: esperando tu confirmación"
    },
    "drops": {
      "check.time_odd": "La hora indicada ({{hora}}) es poco habitual. Confirma con el invitado que no sea un error de tecleo.",
      "check.past": "La fecha de grabación indicada ({{data}}) ya pasó. Confirma la fecha con el invitado.",
      "check.whatsapp_mismatch": "El WhatsApp indicado termina en {{agora}}, pero el anotado en la invitación termina en {{antes}}. Confirma cuál es el correcto.",
      "whatsapp": "El número de WhatsApp informado no fue reconocido{{end}}. Confírmalo con el invitado.",
      "whatsapp_end": " (termina en {{digits}})",
      "accessibility": "El invitado escribió algo sobre accesibilidad, pero no marcó la autorización para ese tipo de dato, así que se descartó. Si es importante para la grabación, pregúntale directamente.",
      "sensitive": "Un dato personal sensible se descartó porque el invitado no marcó la autorización específica.",
      "scheduled_at": "No se pudo leer la fecha de grabación. Confírmala con el invitado.",
      "previous_interviews": "En el campo de entrevistas anteriores había una respuesta que no era un enlace; se ignoró.",
      "links": "Uno de los enlaces no era una dirección válida y se ignoró.",
      "key_ideas": "El invitado envió más de 3 ideas principales; se quedaron las 3 primeras.",
      "other": "Se ignoró una respuesta del campo \"{{field}}\"."
    },
    "held": "Respuesta sin código de invitación válido: no se envió nada al invitado. Si lo invitaste tú, confírmalo desde el menú o con confirmarIntake."
  },
  "sheet": {
    "tab": "Invitados",
    "columns": [
      "Respondió el",
      "Nombre",
      "Cómo prefiere que le llamen",
      "Cargo / actividad",
      "Presentación",
      "Ideas principales",
      "Quiere divulgar",
      "Acepta debatir",
      "Prefiere no tratar",
      "Grabación",
      "Modalidad",
      "Correo",
      "WhatsApp",
      "Contacto preferido",
      "Revisión antes de publicar",
      "Lo que ya se envió",
      "Necesita atención",
      "Briefing",
      "Código del registro"
    ],
    "not_informed": "no informado o no reconocido",
    "none": "—",
    "briefing_link": "Abrir el briefing"
  },
  "menu": {
    "forget_yes": "Olvidar a {{nome}}",
    "window": {
      "cancel": "Cancelar",
      "not_now": "Ahora no",
      "continue": "Continuar",
      "working": "Trabajando…",
      "failed": "Algo salió mal al hablar con Google. Cierra esta ventana e inténtalo de nuevo.",
      "ok": "Cerrar",
      "copy": "Copiar",
      "copied": "Copiado ✓",
      "open": "Abrir"
    },
    "start": {
      "guide": "Guía con imágenes, pantalla por pantalla (en inglés):",
      "tab": "Empieza aquí",
      "title": "Empieza aquí: de cero a la primera invitación en unos 15 minutos",
      "steps": [
        "Esta es tu copia de la hoja de PodFácil. Es solo tuya: nadie más ve lo que pongas aquí.",
        "En el chat de Claude, pide: \"configurar mi programa en PodFácil\". Claude hace las preguntas y guarda el perfil del programa.",
        "Aquí en la hoja, usa el menú PodFácil (arriba, junto a Ayuda). Plan de pago: PodFácil > Activar licencia. Plan gratuito: PodFácil > Configurar programa y escribe el código que mostró Claude. Si el menú no aparece, recarga la página.",
        "La primera vez, Google pide autorización y muestra la pantalla \"Google no ha verificado esta aplicación\", con TU correo como desarrollador. Es lo esperado: la copia es tuya y PodFácil funciona dentro de tu cuenta. Haz clic en Avanzado, después en \"Ir a PodFácil — planilha do programa (no seguro)\" y en Continuar; en la lista de permisos, deja todo marcado y haz clic en Continuar. La ventana se cierra sola y, por lo general, la opción que elegiste continúa sola; si no aparece nada en unos segundos, vuelve a hacer clic en la opción del menú.",
        "Lo que pide Google y lo que hace PodFácil: Google pide acceso a tus hojas de cálculo, formularios y calendarios porque no tiene un permiso más limitado para esto, pero PodFácil solo toca esta hoja, el formulario del invitado y los eventos de grabación que crea; en Drive, solo los archivos que crea él mismo. También envía correos en tu nombre (invitaciones y avisos), comprueba tu licencia en el servidor de PodFácil y funciona solo una vez al día (recordatorios y cola de invitaciones). No lee tus correos.",
        "Con el programa configurado, PodFácil crea el formulario del invitado. Después, en la pestaña Invitaciones, escribe una fila por invitado (nombre y correo bastan) y usa PodFácil > Invitar.",
        "Cuando el invitado responda, llega un aviso a tu correo y la respuesta aparece en la pestaña Invitados."
      ],
      "footer": "¿Dudas o algo raro? Usa PodFácil > Verificar instalación o pregunta a Claude en el chat."
    },
    "invite": "Invitar (pestaña Invitaciones)",
    "confirm_guest": "Enviar confirmación al invitado seleccionado",
    "invites": {
      "wait": "Revisando la pestaña Invitaciones…",
      "send_button": "Enviar {{n}} invitación(es)",
      "wait_send": "Enviando las invitaciones…",
      "busy": "La cola de invitaciones ya se está ejecutando. Espera unos minutos y mira la columna Estado.",
      "tab": "Invitaciones",
      "columns": [
        "Nombre",
        "Correo",
        "Fecha y hora",
        "Modalidad",
        "Enlace de la sala (remota)",
        "WhatsApp (opcional)",
        "Estado"
      ],
      "note": "Una fila por invitado: nombre y correo bastan; fecha, modalidad, enlace y WhatsApp cuando los sepas. Después usa PodFácil > Invitar. La columna Estado la rellena PodFácil.",
      "created": "Creé la pestaña {{aba}}. Rellena una fila por invitado (nombre y correo bastan) y usa PodFácil > Invitar de nuevo.",
      "nothing": "No hay invitaciones pendientes en la pestaña {{aba}}. Las filas con ✅ o ➖ ya se trataron: la misma persona no recibe dos veces la invitación para la misma fecha.",
      "confirm": "¿Enviar {{n}} invitación(es) ahora?",
      "done": "Listo.",
      "done_lines": {
        "enviados": "✅ Invitaciones enviadas: {{n}}",
        "pulados": "➖ Ya la habían recibido (no reenviada): {{n}}",
        "corrigir": "❌ Para corregir (mira la columna Situación): {{n}}",
        "falhas": "⚠️ Con error (usa Invitar de nuevo): {{n}}",
        "depois": "⏳ Quedaron para después: {{n}}"
      },
      "later": "Las que quedaron para después salen solas mañana, a la hora del recordatorio diario.",
      "need_form": "Antes de invitar, el programa debe estar configurado y el formulario creado. Usa PodFácil > Verificar instalación.",
      "status": {
        "unsure": "⚠️ Sin confirmación de envío (la ronda se interrumpió): revisa Enviados en Gmail; si no salió, usa Invitar de nuevo",
        "sent": "✅ Enviada el {{quando}}",
        "sent_logo": "✅ Enviada el {{quando}}, sin el logo (usa PodFácil > Subir logo)",
        "already": "➖ Ya se había enviado",
        "optout": "➖ No enviada: la persona pidió no recibir correos",
        "quota": "⏳ En cola: se acabó la cuota de correos de hoy; sale mañana",
        "time": "⏳ En cola: sale en la próxima ronda",
        "failed": "⚠️ Falló: {{motivo}}. Usa Invitar de nuevo para reintentar",
        "fix": "❌ Corrige: {{motivo}}"
      },
      "errors": {
        "past": "la fecha ya pasó",
        "name": "falta el nombre",
        "email": "correo no válido",
        "date": "fecha y hora no reconocidas (usa 20/10/2026 14:30)",
        "mode": "modalidad no reconocida (usa {{modos}})",
        "link": "el enlace de la sala debe empezar por https://",
        "whatsapp": "WhatsApp no reconocido (usa +código de país y número)"
      },
      "digest_subject": "Cola de invitaciones: {{enviados}} enviada(s) hoy",
      "digest_body": "La cola de invitaciones se ejecutó sola hoy. Enviadas: {{enviados}} · por corregir: {{corrigir}} · con fallo: {{falhas}} · aún en cola: {{depois}}. Mira la pestaña {{aba}}: {{url}}"
    },
    "confirm": {
      "send_button": "Enviar la confirmación",
      "wait": "Enviando…",
      "busy": "Esta confirmación ya está saliendo; no hace falta volver a hacer clic.",
      "held": "Esta respuesta está retenida (llegó sin código de invitación válido). Confirma al invitado antes de enviarle un correo.",
      "title": "Enviar confirmación",
      "ask": "¿Enviar a {{nome}} un correo pidiendo que confirme {{n}} punto(s)?\n\n{{itens}}",
      "ask_none": "No encontré nada que corregir en las respuestas de {{nome}}. ¿Enviar de todos modos un correo para que confirme sus datos?",
      "again": "Ya se envió una confirmación el {{quando}}.",
      "done": "Confirmación enviada a {{nome}}. La respuesta llegará a tu correo.",
      "optout": "{{nome}} pidió no recibir correos del programa; no se envió nada.",
      "quota": "Se acabó la cuota de correos de hoy. Inténtalo mañana.",
      "not_found": "No encontré las respuestas de este invitado (código {{id}})."
    },
    "title": "PodFácil",
    "activate_license": "Activar licencia",
    "check_install": "Verificar instalación",
    "resend_notice": "Reenviar aviso del invitado seleccionado",
    "rebuild_guests": "Rehacer pestaña Invitados",
    "forget_guest": "Olvidar invitado seleccionado (privacidad)",
    "release_devices": "Liberar otros dispositivos",
    "ask_code_title": "¿Qué invitado?",
    "ask_code": "En la pestaña Invitados, haz clic en la fila del invitado y elige la opción de nuevo. O pega aquí el código del registro (última columna):",
    "resend_done": "Aviso reenviado a tu correo.",
    "rebuild_done": "Pestaña Invitados rehecha, con los enlaces del briefing conservados.",
    "forget_confirm": "¿Olvidar a {{nome}}? Borra las respuestas, la fila de Invitados y el evento de la agenda, y envía el briefing a la papelera. No se puede deshacer.",
    "forget_done": "Listo: {{nome}} fue olvidado.",
    "forget_pending": "Falta hacer a mano:",
    "error": "No funcionó: {{motivo}}",
    "license": {
      "plans": {
        "free": "Gratis",
        "individual_solo": "Individual Solo",
        "individual_duo": "Individual Duo",
        "enterprise_10": "Estudio, hasta 10 personas",
        "enterprise_20": "Estudio, hasta 20 personas"
      },
      "upgrade_hint": "Tu licencia libera el formulario completo: para cambiar el esencial por él, usa Verificar instalación.",
      "ok_stay": "Licencia activada (plan {{plano}}). Copia lo que necesites arriba y cierra esta ventana.",
      "ok_read": "Licencia activada (plan {{plano}}). Lee el aviso de abajo y cierra esta ventana.",
      "title": "Activar licencia de PodFácil",
      "lead": "Pega la clave que recibiste por correo después de la compra. Se guarda solo en este proyecto y no aparece en pantalla.",
      "label": "Clave de licencia",
      "button": "Activar",
      "working": "Comprobando con el servidor…",
      "ok": "Licencia activada (plan {{plano}}). Esta ventana se cierra sola.",
      "saved_offline": "Clave guardada. El servidor de PodFácil no respondió ahora; se comprobará en el próximo uso.",
      "invalid": "Eso no parece una clave de licencia. La clave empieza con pgi_ y tiene 47 letras, números, - y _. En el correo, no hagas doble clic (se detiene en el primer guion): selecciona arrastrando del inicio al final de la clave, copia y pégala aquí.",
      "refused": "El servidor rechazó la clave: {{motivo}}",
      "free_key": "Esa clave está en el plan gratuito. Las automatizaciones son del plan de pago.",
      "saved_limit": "Clave guardada. Llegó al límite de ordenadores: usa PodFácil > Liberar otros dispositivos.",
      "offline_keep": "El servidor de PodFácil no respondió ahora y ya hay una clave guardada; sigue vigente. Intenta cambiarla de nuevo en unos minutos.",
      "unknown": "El servidor no reconoce esta clave. Comprueba que copiaste la clave completa del correo.",
      "failed": "Algo salió mal al hablar con Google. Cierra esta ventana e inténtalo de nuevo."
    },
    "check": {
      "wait": "Verificando la instalación…",
      "form_ask_yes": "Crear el formulario",
      "form_gone_yes": "Crear uno nuevo",
      "upgrade_yes": "Cambiar al completo",
      "form_gone_ask": "El formulario registrado no abre (borrado o sin acceso). ¿Crear uno nuevo ahora? El enlace del invitado cambia; las respuestas ya recibidas siguen en la hoja.",
      "upgrade_ask": "Tu licencia de pago libera el formulario completo. ¿Cambiar ahora? El enlace del invitado cambia: el antiguo deja de aceptar respuestas, y las respuestas ya recibidas siguen en la hoja.",
      "form_ask": "Todavía no hay formulario del invitado. ¿Crearlo ahora? (tarda unos segundos)",
      "phone_ok": "WhatsApp del formulario con validación (un número incompleto o con letras no pasa)",
      "title": "Verificar instalación",
      "summary_ok": "Todo bien con PodFácil.",
      "summary_fail": "{{n}} punto(s) te necesitan:",
      "show_ok": "Configuración del programa: {{nome}}.",
      "show_missing": "Falta la configuración del programa (Claude la prepara contigo).",
      "form_ok": "Formulario del invitado encontrado.",
      "form_missing": "El formulario aún no se ha creado.",
      "form_gone": "El formulario registrado no abre (borrado o sin acceso).",
      "triggers_ok": "Envíos automáticos activos.",
      "triggers_fixed": "Los envíos automáticos estaban apagados y se reactivaron.",
      "guests_ok": "Pestaña Invitados en su lugar.",
      "guests_fixed": "La pestaña Invitados no existía y se creó.",
      "guests_fail": "No pude crear la pestaña Invitados: {{motivo}}",
      "license_none": "Sin licencia: plan gratuito. Para el plan de pago, usa PodFácil > Activar licencia.",
      "license_paid": "Licencia activa (plan {{plano}}).",
      "license_offline": "Licencia guardada; el servidor no respondió ahora.",
      "license_fail": "Problema con la licencia: {{motivo}}",
      "triggers_other": "Los envíos automáticos los activó la cuenta {{dono}}. Pide a esa persona que abra PodFácil > Verificar instalación.",
      "logo_fail": "PodFácil no puede abrir el logo de Drive; las invitaciones salen con el nombre del programa en su lugar. Súbelo de nuevo en PodFácil > Subir logo.",
      "logo_ok": "Logo de la invitación en su lugar."
    },
    "devices": {
      "confirm_yes": "Liberar los dispositivos",
      "title": "Liberar otros dispositivos",
      "confirm": "Esto desconecta todos los ordenadores vinculados a tu licencia; cada uno vuelve a funcionar en su próximo uso. Vale 2 veces al mes. ¿Continuar?",
      "done": "Dispositivos liberados.",
      "no_key": "Activa la licencia primero (PodFácil > Activar licencia)."
    },
    "config": {
      "tz_label": "Zona horaria de las fechas",
      "ask_code_button": "Configurar",
      "wait_profile": "Buscando el perfil del programa…",
      "wait_form": "Creando el formulario del invitado en Google Forms. Tarda de 1 a 2 minutos: puedes dejar esta ventana abierta.",
      "form_link": "Enlace del formulario del invitado",
      "form_busy": "El formulario ya se está creando en otra ventana. Espera un minuto y usa Verificar instalación.",
      "form_exists": "El formulario del invitado ya existe. Enlace para el invitado: {{url}}",
      "form_created": "Formulario del invitado creado ({{variante}}). Enlace para el invitado: {{url}} El enlace también queda guardado en la pestaña Configuración.",
      "form_fail": "No pude crear el formulario: {{motivo}}",
      "variants": {"essencial": "esencial", "completo": "completo"},
      "item": "Configurar programa",
      "ask_code_title": "Código del programa",
      "ask_code": "Escribe el código de 15 letras y números que Claude mostró en el chat (con o sin los guiones):",
      "done": "Programa \"{{nome}}\" configurado. Los datos están en la pestaña {{aba}}.",
      "tab": "Configuración",
      "note": "Esta pestaña solo muestra la configuración. Para cambiarla, pídeselo a Claude en el chat y usa PodFácil > Configurar programa de nuevo.",
      "labels": {
        "name": "Programa",
        "tagline": "Frase de presentación",
        "locale": "Idioma",
        "editorial": "Línea editorial",
        "modes": "Graba en",
        "studio": "Estudio",
        "address": "Dirección",
        "colors": "Colores",
        "logo": "Logo",
        "controller": "Responsable de los datos",
        "retention": "Conservación de respuestas"
      },
      "retention_days": "{{dias}} días después de publicar",
      "imported": "Perfil del programa \"{{nome}}\" importado.",
      "logo_item": "Subir logo",
      "import_failed": "El perfil del programa llegó, pero no pude guardarlo ({{motivo}}). Pide a Claude que lo guarde de nuevo y usa PodFácil > Configurar programa.",
      "logo": {
        "title": "Logo de la invitación",
        "lead": "Elige el logo del programa (PNG o JPG, hasta 1 MB). Va incrustado en las invitaciones y se guarda en tu Google Drive.",
        "button": "Subir",
        "working": "Subiendo…",
        "ok": "Logo guardado. Las próximas invitaciones ya salen con él.",
        "too_big": "El archivo supera 1 MB. Reduce la imagen e inténtalo de nuevo.",
        "bad_type": "Usa un archivo PNG o JPG.",
        "need_show": "Configura el programa primero (PodFácil > Configurar programa).",
        "failed": "Algo salió mal al subir el logo. Inténtalo de nuevo."
      }
    }
  },
  "guest_confirm": {
    "subject": "{{show}}: ¿puedes confirmar algunos datos de tu participación?",
    "greeting": "¡Hola, {{nome}}!",
    "intro": "Gracias por responder al formulario de {{show}}. Antes de la grabación, queremos confirmar algunos puntos:",
    "intro_none": "Gracias por responder al formulario de {{show}}. Antes de la grabación, queremos confirmar los datos de abajo.",
    "items": {
      "contacts.whatsapp": "No pudimos leer el número de WhatsApp que indicaste{{end}}. ¿Cuál es el número correcto, con código de país?",
      "accessibility": "Escribiste algo sobre accesibilidad, pero no marcaste la autorización para guardar este tipo de información, así que no se registró. Si quieres que nos preparemos, responde a este correo y acordamos cómo hacerlo.",
      "scheduled_at": "No pudimos leer la fecha y la hora de la grabación. ¿Cuándo te viene bien?",
      "check.time_odd": "La hora que indicaste fue {{hora}}. ¿Es correcta?",
      "check.past": "La fecha indicada ({{data}}) ya pasó. ¿Cuál es la fecha correcta?",
      "check.whatsapp_mismatch": "El WhatsApp que indicaste termina en {{agora}}, pero teníamos anotado uno que termina en {{antes}}. ¿Cuál usamos?"
    },
    "end": " (termina en {{digits}})",
    "summary": "Lo que tenemos anotado",
    "labels": {
      "recording": "Grabación",
      "whatsapp": "WhatsApp"
    },
    "whatsapp_end": "termina en {{digits}}",
    "closing": "Basta con responder a este correo con la corrección. Si todo está bien, responde \"está bien\".",
    "signature": "Equipo de {{show}}"
  }
}

```


## pt-BR.json

```json
{
  "locale": "pt-BR",
  "needs_native_review": false,
  "text_version": "pt-BR/v1",
  "form": {
    "validation": {
      "phone": "Digite o número com DDD, ex.: 11 91234-5678 (ou +55 11 91234-5678)."
    },
    "title": "Convidado(a) do {{show.name}}",
    "description_essencial": "Leva uns 2 minutos. Com isso a gente prepara uma conversa boa para você, sem surpresa.",
    "description_completo": "Leva uns 8 minutos. Quase tudo é opcional: pule o que não quiser responder.",
    "confirmation": "Obrigado! Se você autorizou o e-mail, o kit do convidado chega em instantes. Para mandar arquivos (PDF, slides, fotos), é só responder a esse e-mail com os anexos.",
    "sections": {
      "about": "Sobre você",
      "content": "A conversa",
      "logistics": "Gravação",
      "channels": "Como falamos com você",
      "consent": "Seus dados e esta entrevista",
      "sensitive": "Dados sensíveis (opcional)",
      "localization": "Outros idiomas (opcional)"
    },
    "fields": {
      "guest.full_name": { "title": "Nome completo", "help": "" },
      "guest.preferred_name": { "title": "Como quer ser chamado(a) no ar?", "help": "Ex.: Ana, Dra. Ana, Professor Silva." },
      "guest.name_pronunciation": { "title": "Como se pronuncia seu nome?", "help": "Só se houver risco de errarmos." },
      "guest.pronouns": { "title": "Pronomes", "help": "Opcional. Ex.: ela/dela." },
      "guest.role_title": { "title": "Cargo ou ocupação", "help": "" },
      "guest.photo_url": { "title": "Link de uma foto sua para a divulgação", "help": "Opcional. Um link público (site, LinkedIn, Drive aberto)." },
      "bio.short": { "title": "Mini-bio em até 2 linhas", "help": "É o que vamos ler na abertura." },
      "bio.long": { "title": "Bio completa", "help": "Opcional." },
      "links": { "title": "Seus links principais", "help": "Site, perfis, portfólio. Um por linha. Se não tiver, deixe em branco." },
      "social_handles": { "title": "@ para marcarmos na divulgação", "help": "Um por linha, no formato rede: @usuario (ex.: instagram: @ana)." },
      "previous_interviews": { "title": "Entrevistas que você já deu", "help": "Links, um por linha. Ajuda a não repetir perguntas." },
      "key_ideas": { "title": "Até 3 ideias que você quer deixar para o público", "help": "Uma por linha." },
      "stories_to_tell": { "title": "Histórias que você gosta de contar", "help": "Uma por linha." },
      "controversies.accepts": { "title": "Temas polêmicos que você topa discutir", "help": "Um por linha." },
      "controversies.declines": { "title": "Temas polêmicos que prefere evitar", "help": "Um por linha." },
      "off_limits_topics": { "title": "Assuntos proibidos", "help": "Não vamos tocar nesses temas. Um por linha." },
      "wants_to_promote": { "title": "Algo que quer divulgar?", "help": "Livro, curso, evento, projeto. Um por linha." },
      "dream_questions": { "title": "Perguntas que você adoraria receber", "help": "Uma por linha." },
      "conflicts_of_interest.details": { "title": "Conflitos de interesse ou patrocínios ligados aos temas", "help": "Deixe em branco se não houver." },
      "companion.name": { "title": "Vai trazer acompanhante? Quem?", "help": "Deixe em branco se vier sozinho(a)." },
      "materials": { "title": "Materiais de apoio (links)", "help": "Palestras, livros, artigos, vídeos. Um link por linha. Arquivos: responda ao e-mail do kit com os anexos." },
      "recording_mode": { "title": "Como vai ser a gravação?", "help": "" },
      "scheduled_at": { "title": "Data e hora já combinadas com a gente", "help": "Só se já combinou. Serve para o convite na agenda e o lembrete na véspera." },
      "wants_prepublication_review": { "title": "Quer ver o episódio antes de publicarmos?", "help": "" },
      "preferred_channel": { "title": "Canal preferido para falarmos com você", "help": "" },
      "contacts.email": { "title": "Seu e-mail", "help": "" },
      "invite.token": { "title": "Código do convite", "help": "Já vem preenchido pelo link do convite que você recebeu por e-mail. Não altere. Se estiver vazio, responda mesmo assim: o programa confere com você antes de enviar qualquer coisa." },
      "contacts.whatsapp": { "title": "Seu WhatsApp", "help": "Opcional. Com código do país e DDD, ex.: +55 11 91234-5678." },
      "automation_consents": { "title": "Posso usar estes canais para te mandar o kit e os lembretes?", "help": "Marque só o que quiser. Nada marcado = nada enviado por aquele canal." },
      "image_voice": { "title": "Imagem e voz", "help": "" },
      "consent.general": { "title": "Consentimento", "help": "" },
      "consent.public_research": { "title": "Pesquisa em fontes públicas", "help": "" },
      "consent.divulgacao": { "title": "Divulgação (opcional)", "help": "" },
      "accessibility.needs": { "title": "DADO SENSÍVEL — Precisa de alguma adaptação de acessibilidade?", "help": "Opcional. Pode revelar informação de saúde: só será usado se você marcar o aceite logo abaixo." },
      "accessibility.accept": { "title": "DADO SENSÍVEL — Aceite específico (acessibilidade)", "help": "" },
      "sensitive.category": { "title": "DADO SENSÍVEL — Sobre o que é?", "help": "Opcional." },
      "sensitive.value": { "title": "DADO SENSÍVEL — O que você quer que a gente saiba", "help": "Opcional. Escreva só o que quiser que entre na preparação." },
      "sensitive.accept": { "title": "DADO SENSÍVEL — Aceite específico", "help": "" },
      "localization.translation_text": { "title": "Legendas e textos traduzidos", "help": "" },
      "localization.dub_generic_voice": { "title": "Dublagem com voz sintética genérica", "help": "" },
      "localization.dub_voice_replica": { "title": "DADO SENSÍVEL — Réplica artificial da sua voz", "help": "" }
    },
    "choices": {
      "recording_mode": { "presencial": "Presencial, no estúdio", "remoto": "Remota, online" },
      "yes_no": { "yes": "Sim", "no": "Não" },
      "preferred_channel": { "email": "E-mail", "whatsapp": "WhatsApp", "phone": "Telefone", "other": "Outro" },
      "channels": {
        "email": "E-mail: kit do convidado e lembrete na véspera",
        "whatsapp": "WhatsApp: kit e lembrete na véspera",
        "calendar": "Agenda: convite com data e endereço"
      },
      "sensitive_category": {
        "origem_racial_etnica": "Origem racial ou étnica",
        "conviccao_religiosa": "Convicção religiosa",
        "opiniao_politica": "Opinião política",
        "filiacao_sindical_religiosa_filosofica_politica": "Filiação a sindicato ou organização religiosa, filosófica ou política",
        "saude": "Saúde",
        "vida_sexual": "Vida sexual",
        "genetico": "Dado genético",
        "biometrico": "Dado biométrico"
      }
    }
  },
  "consent": {
    "contact_email": "pelo e-mail {{email}}",
    "contact_reply_to_email": "respondendo a qualquer e-mail deste programa (inclusive o convite ou o kit do convidado)",
    "clauses": {
      "BR-LGPD": {
        "clause_id": "BR-LGPD/v1",
        "legal_review": "pendente",
        "text": "{{controller.name}} (controlador dos dados{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contato: {{controller.contact}}) vai usar as respostas deste formulário somente para as finalidades abaixo, ligadas à sua entrevista no {{show.name}}: {{purposes}}.\n\nPara preparar perguntas melhores, também vamos consultar informações que você mesmo(a) tornou públicas (site, redes, entrevistas e textos publicados). Tudo o que entrar no material de preparo terá a fonte indicada.\n\nNão vamos usar nem guardar dados sensíveis (saúde, religião, opinião política, vida sexual, origem racial ou étnica, entre outros), a menos que você mesmo(a) os escreva na seção opcional de dados sensíveis e marque o aceite específico de cada um. A decisão é sua.\n\nOs dados são apagados até {{retention_days}} dias após a publicação do episódio; guardamos só o registro deste consentimento, como prova. A qualquer momento e sem custo você pode pedir acesso, correção ou exclusão, ou retirar este consentimento, {{controller.contact}}. Se não quiser consentir, basta não enviar o formulário: a entrevista ainda pode acontecer, sem o uso dele."
      },
      "EU-GDPR": {
        "clause_id": "EU-GDPR/v1",
        "legal_review": "pendente",
        "text": "{{controller.name}} (controlador dos dados{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contato: {{controller.contact}}) vai tratar as respostas deste formulário com base no seu consentimento, somente para: {{purposes}}.\n\nTambém vamos consultar informações que você tornou publicamente acessíveis (site, redes, entrevistas, textos publicados), sempre com a fonte indicada.\n\nDados de categorias especiais (saúde, religião, opinião política, vida sexual, origem racial ou étnica, entre outros) só serão tratados se você os escrever na seção opcional e der o consentimento explícito de cada um.\n\nOs dados são apagados até {{retention_days}} dias após a publicação do episódio. Você tem direito de acesso, retificação, apagamento, limitação, portabilidade e oposição, e pode retirar o consentimento a qualquer momento ({{controller.contact}}), sem afetar o tratamento já feito. Você também pode reclamar a uma autoridade de controle."
      },
      "other": {
        "clause_id": "other/v1",
        "legal_review": "pendente",
        "text": "{{controller.name}} (contato: {{controller.contact}}) vai usar as respostas deste formulário somente para: {{purposes}}. Também vamos consultar informações que você tornou públicas, sempre com fonte. Dados sensíveis só entram se você os escrever na seção opcional e marcar o aceite específico. Os dados são apagados até {{retention_days}} dias após a publicação. Para acessar, corrigir, apagar ou retirar o consentimento: {{controller.contact}}."
      }
    },
    "purposes": {
      "preparo_entrevista": "preparar a sua entrevista",
      "dossie": "montar o material de preparo (com fontes)",
      "memoria_episodio": "registrar o episódio no arquivo do programa",
      "divulgacao": "divulgar o episódio com sua mini-bio, foto e @"
    },
    "draft_notice": "AVISO: este texto de consentimento é um RASCUNHO (v0) em revisão jurídica e pode mudar. Se a versão final mudar algo, vamos pedir o seu aceite de novo.",
    "general_accept": "Li o texto acima e concordo com o uso das minhas respostas para essas finalidades.",
    "public_research_accept": "Estou ciente de que haverá consulta a informações que eu mesmo(a) tornei públicas, sempre com fonte indicada.",
    "divulgacao_accept": "Também autorizo usar minha mini-bio, foto e @ na divulgação do episódio.",
    "image_voice_accept": "Autorizo a gravação e a publicação da minha imagem e voz neste episódio.",
    "sensitive_intro": "Esta seção é totalmente opcional e a decisão é sua. Tudo aqui é DADO SENSÍVEL (LGPD, art. 11): só será usado se você escrever e marcar o aceite específico logo abaixo de cada campo. Sem o aceite, a informação é descartada e não é guardada.",
    "sensitive_accept": "DADO SENSÍVEL — Autorizo, de forma específica e destacada, o uso da informação que escrevi acima apenas para preparar e conduzir esta entrevista.",
    "accessibility_accept": "DADO SENSÍVEL (pode revelar saúde) — Autorizo usar a necessidade de acessibilidade acima apenas para organizar a logística da gravação.",
    "sensitive_purpose": "preparar e conduzir esta entrevista",
    "accessibility_purpose": "organizar a logística da gravação",
    "localization_intro": "Esta seção é opcional e cada autorização é separada: marque só o que quiser. Nenhuma delas é condição para a entrevista, e nenhuma vem marcada. Você pode retirar qualquer uma a qualquer momento, sem custo, pelo mesmo contato indicado na seção de dados.",
    "translation_accept": "Autorizo transcrever minha fala e publicar legendas e textos traduzidos deste episódio (inclusive a descrição) em: {{locales}}.",
    "dub_generic_accept": "Autorizo uma versão dublada deste episódio com voz sintética genérica (não é a minha voz), dizendo a tradução da minha fala, identificada ao público como dublagem por IA, em: {{locales}}.",
    "dub_replica_accept": "DADO SENSÍVEL (LGPD, art. 11) — Autorizo, de forma específica e destacada, criar uma réplica artificial da minha voz somente para dublar ESTE episódio em {{locales}}, pelo provedor {{provider}} ({{country}}), com o modelo da minha voz apagado em até {{days}} dias após a dublagem. A versão dublada será identificada ao público como feita por IA. Posso revogar a qualquer momento.",
    "dub_replica_purpose": "dublar este episódio com réplica artificial da voz do titular"
  },
  "kit": {
    "title": "Kit do convidado",
    "greeting": "Olá, {{guest.preferred_name}}!",
    "thanks": "Que bom ter você no {{show.name}}. Este kit junta o que você precisa saber antes da gravação. Leia com calma, quando puder.",
    "about_heading": "O que é o {{show.name}}",
    "pillars_heading": "Os temas que circulam por aqui",
    "when_heading": "Quando",
    "when_tbd": "A data ainda vai ser combinada com a produção.",
    "where_heading": "Onde (gravação presencial)",
    "address_label": "Endereço",
    "landmarks_label": "Pontos de referência",
    "gps_label": "No GPS ou no app de transporte, digite",
    "parking_label": "Estacionamento",
    "arrive": "Chegue de {{arrive.min}} a {{arrive.max}} minutos antes, para tomar uma água e testar o som sem pressa.",
    "remote_heading": "Gravação remota: o que você precisa",
    "remote_default": [
      "Fone de ouvido (com fio, se tiver)",
      "Lugar silencioso e com pouco eco",
      "Internet estável; se puder, cabo em vez de Wi-Fi",
      "Computador carregado ou na tomada"
    ],
    "conduct_heading": "Para você ficar tranquilo(a)",
    "conduct_default": [
      "Não existe resposta errada: é uma conversa, não uma prova.",
      "Se travar ou quiser refazer uma resposta, é só dizer. A gente edita.",
      "Você pode pedir para não falar de um assunto a qualquer momento.",
      "Água à vontade, e pausas também."
    ],
    "materials_heading": "Materiais (opcional)",
    "materials_text": "Quer mandar slides, PDFs, fotos ou links? Responda a este e-mail com os anexos. Não precisa criar conta em lugar nenhum.",
    "privacy_heading": "Seus dados",
    "privacy_text": "Usamos suas respostas só para preparar esta entrevista. Para acessar, corrigir, apagar ou retirar o consentimento: {{controller.contact}}.",
    "signoff": "Até já!",
    "parking": {
      "disponivel": "disponível no local",
      "indisponivel": "não há estacionamento no local",
      "pago_proximo": "estacionamento pago nas proximidades",
      "pendente": "a confirmar com a produção"
    }
  },
  "messages": {
    "email_subject": "Kit do convidado · {{show.name}}",
    "owner_subject": "✅ {{guest.preferred_name}} respondeu ao formulário · {{show.name}}",
    "calendar_title": "Gravação {{show.name}} com {{guest.preferred_name}}",
    "calendar_remote_location": "Online (o link vem da produção)",
    "calendar_description": "Kit do convidado enviado por e-mail. Dúvidas: {{controller.contact}}.",
    "whatsapp_kit": "Olá, {{guest.preferred_name}}! Aqui é do {{show.name}}. Recebemos seu formulário, obrigado! O kit do convidado com todos os detalhes foi para o seu e-mail.{{#address_line}} Endereço: {{address_line}}.{{/address_line}}{{#gps_hint}} No GPS, digite: {{gps_hint}}.{{/gps_hint}}",
    "reminder_subject": "Amanhã: gravação no {{show.name}}",
    "reminder_body": "Olá, {{guest.preferred_name}}! Lembrete: a gravação no {{show.name}} é amanhã, {{scheduled_text}}.{{#address_line}} Endereço: {{address_line}}.{{/address_line}}{{#gps_hint}} No GPS, digite: {{gps_hint}}.{{/gps_hint}}{{#arrive}} Chegue de {{arrive.min}} a {{arrive.max}} minutos antes.{{/arrive}} Qualquer coisa, é só responder."
  },
  "invitation": {
    "subject": "Convite oficial · {{show.name}}",
    "preheader": "{{show.name}} convida você para uma conversa. Data, local e formulário aqui dentro.",
    "title": "Convite oficial",
    "greeting": "Olá, {{guest.name}}!",
    "intro": {
      "formal": "Temos a honra de convidar você para participar como convidado(a) do {{show.name}}.",
      "cordial": "É uma alegria convidar você para uma conversa no {{show.name}}.",
      "descontraido": "Bora gravar? A gente quer muito você no {{show.name}}."
    },
    "when_label": "Data e horário",
    "when_tbd": "a combinar com a produção",
    "where_label": "Local",
    "gps_label": "No GPS ou no app de transporte, digite",
    "arrival_label": "Como chegar",
    "arrive": "Chegue de {{arrive.min}} a {{arrive.max}} minutos antes.",
    "remote_label": "Gravação remota, link da sala",
    "remote_link_tbd": "o link da sala chega por e-mail antes da gravação",
    "about_heading": "O que é o {{show.name}}",
    "cta_intro": {
      "essencial": "Para prepararmos uma conversa à sua altura, preencha o formulário do convidado. Leva uns 2 minutos.",
      "completo": "Para prepararmos uma conversa à sua altura, preencha o formulário do convidado. Leva uns 8 minutos, e quase tudo é opcional."
    },
    "cta_button": "Preencher o formulário",
    "cta_fallback": "Se o botão não abrir, copie e cole este endereço no navegador:",
    "signoff": "Com apreço,",
    "footer_controller": "Quem envia: {{controller.name}}, controlador dos dados. Contato: {{controller.contact}}.",
    "footer_purpose": "Você recebeu este convite porque {{signature.name}} indicou você como convidado(a). Usamos seu nome e e-mail só para este convite e para organizar a entrevista; o kit do convidado chega depois que você responder ao formulário.",
    "footer_optout": "Não quer receber mais mensagens do {{show.name}}? Responda a este e-mail com a palavra SAIR e não enviaremos mais nada.",
    "footer_brand": "Preparado com PodFácil",
    "ics_description": "Convite oficial do {{show.name}}. Formulário do convidado: {{form_url}}"
  },
  "decision": {
    "ack": {
      "v1": "Li os alertas acima. Entendo que o plugin apenas recomenda: a decisão de seguir contra a recomendação é minha, e a responsabilidade editorial e jurídica pelo que for gravado e publicado é minha (ou de quem eu represento), não do plugin nem dos seus autores."
    },
    "alerts": {
      "R-CLAIM-CONDUTA-FONTES": "Esta afirmação sobre a conduta de alguém não tem o lastro recomendado (status verificado com 1 fonte primária ou 2 fontes de imprensa independentes). Usá-la no ar pode gerar responsabilidade por difamação.",
      "R-CLAIM-CONDUTA-INDEPENDENCIA": "As fontes de imprensa desta afirmação sobre conduta podem não ser independentes (mesmo domínio, autor ou agência). Confira autor, veículo e agência antes de decidir.",
      "R-ROTEIRO-GATE-PENDENTE": "A revisão do @guardian (fact-check) ainda não foi feita para um modo que a recomenda antes de gravar.",
      "R-ROTEIRO-GATE-AJUSTES": "O @guardian recomendou ajustes que ainda não constam como aplicados.",
      "R-ROTEIRO-GATE-VETADO": "O @guardian recomendou NÃO gravar este roteiro como está. Gravar contra essa recomendação é decisão e responsabilidade sua.",
      "R-ROTEIRO-CONTRADITORIO": "Este modo recomenda ouvir a parte citada antes de gravar, e não há pedido de contraditório registrado.",
      "R-ROTEIRO-REVISAO-JURIDICA": "Este modo tem risco jurídico alto e a revisão jurídica humana recomendada ainda está pendente.",
      "R-ROTEIRO-SEM-LASTRO": "Há afirmações de fato sem claim do dossiê nem fonte. Dizer no ar algo sem lastro é risco editorial seu.",
      "R-ROTEIRO-INFERENCIA-COMO-FATO": "Uma inferência (hipótese) aparece como afirmação de fato. O recomendado é transformá-la em pergunta ou hipótese.",
      "R-ROTEIRO-RIGOR": "O modo pede fonte para números, datas e citações, e esta afirmação se apoia só no que foi autodeclarado.",
      "R-ROTEIRO-DEGRADADO": "O dossiê veio incompleto e este bloco usa afirmações dele sem ressalva de confirmação com o convidado.",
      "R-ROTEIRO-TIMING": "A soma dos tempos dos blocos se afasta mais de 15% da duração alvo.",
      "R-FACTCHECK-SEM-FONTE": "O fact-check não encontrou fonte para esta afirmação.",
      "R-FACTCHECK-DISCLOSURE": "Falta a identificação de publicidade ou patrocínio recomendada (CONAR / CDC art. 36).",
      "R-LOCALIZACAO-REVISAO-HUMANA": "Tradução automática: revise original e tradução lado a lado (nomes, números, termos do glossário) antes de publicar.",
      "R-LOCALIZACAO-SEM-ACEITE-TRADUCAO": "Não há aceite registrado do convidado para legendas e textos traduzidos neste idioma. Publicar assim é decisão e responsabilidade sua.",
      "R-LOCALIZACAO-SEM-ACEITE-VOZ-GENERICA": "Não há aceite registrado do convidado para dublagem com voz sintética genérica neste idioma. Publicar assim é decisão e responsabilidade sua.",
      "R-LOCALIZACAO-AGENTE-POLITICO": "O convidado foi marcado como candidato ou agente político. Conteúdo sintético com voz de candidatos tem regras próprias da Justiça Eleitoral (Res. TSE 23.732/2024; fonte secundária, conferir o texto vigente): verifique calendário eleitoral e rotulagem antes de publicar a dublagem.",
      "R-LOCALIZACAO-GLOSSARIO": "Termos do glossário do show não aparecem como esperado na tradução (nome próprio, sigla ou termo que não se traduz).",
      "R-LOCALIZACAO-NUMEROS": "Há números do original (datas, alíquotas, artigos de lei) que não aparecem na tradução.",
      "R-LOCALIZACAO-CPS": "Algumas legendas passam do limite de leitura (caracteres por segundo).",
      "R-FACTCHECK-LGPD": "Há dado pessoal de terceiro citado sem base clara de tratamento. (Dado sensível não autodeclarado não é alerta: é proibido.)",
      "R-PUBLICACAO-GATE": "O quality gate do episódio não recomendou a publicação (REQUEST CHANGES ou HOLD).",
      "R-MEMORIA-ROTEIRO-PENDENTE": "Nenhum roteiro ligado a este episódio está pronto para gravar (pronto_para_gravar). Gravar assim é decisão e responsabilidade sua."
    }
  },
  "localization": {
    "language_names": {
      "pt-BR": "português",
      "en": "inglês",
      "es": "espanhol",
      "zh": "chinês"
    },
    "disclosure": {
      "subtitles": "Tradução automática revisada por {{show}}.",
      "dub_generic": "Versão dublada por inteligência artificial a partir do episódio original em {{source_language}}. As vozes são sintéticas.",
      "dub_replica": "Versão dublada por inteligência artificial, com réplica autorizada da voz dos participantes, a partir do episódio original em {{source_language}}."
    }
  },
  "owner": {
    "failed": {
      "subject": "PodFácil: uma resposta do formulário não foi processada",
      "body": "Chegou uma resposta no formulário do convidado em {{quando}}, mas o PodFácil não conseguiu processá-la.\n\nMotivo: {{motivo}}\n\nO convidado pode não ter recebido o kit nem o convite da agenda. A resposta está guardada na aba \"Respostas ao formulário\" da sua planilha. Mostre este e-mail ao Claude no chat para resolver."
    },
    "confirm_hint": "Para pedir a correção ao convidado: na aba Convidados, clique na linha dele e use PodFácil > Enviar confirmação.",
    "headline": "{{name}} respondeu ao formulário.",
    "lead": "Está tudo registrado. Veja abaixo o que já aconteceu e o que a pessoa contou.",
    "happened": "O que já aconteceu",
    "form_received": "Convite recebido e formulário preenchido",
    "attention": "Precisa da sua atenção",
    "summary": "Resumo do convidado",
    "button": "Ver as respostas completas",
    "next_step": "Próximo passo: peça ao Claude \"preparar o briefing de {{name}}\" para receber o dossiê e a pauta.",
    "notes": "Observações",
    "record_code": "Código do registro: {{id}}",
    "full_answers": "Respostas completas: {{url}}",
    "labels": {
      "name": "Nome",
      "prefers": "prefere ser chamado(a) de {{name}}",
      "role": "Cargo / atuação",
      "bio": "Apresentação",
      "ideas": "Ideias principais",
      "recording": "Gravação",
      "email": "E-mail",
      "whatsapp": "WhatsApp"
    },
    "mode": {
      "presencial": "Presencial",
      "remoto": "Remota"
    },
    "date_tbd": "a combinar",
    "sends": {
      "kit_email": "Kit do convidado por e-mail",
      "kit_whatsapp": "Kit do convidado por WhatsApp",
      "calendar": "Convite na agenda",
      "automations": "Envios automáticos (kit e agenda)", "guest": "Envio ao convidado",
      "other": "Envio \"{{key}}\""
    },
    "status": {
      "sent": "{{label}}: enviado",
      "skipped": "{{label}}: não enviado",
      "off": "{{label}}: o WhatsApp não está ligado nesta planilha",
      "error": "{{label}}: falhou",
      "held": "{{label}}: aguardando sua confirmação"
    },
    "drops": {
      "check.time_odd": "O horário informado ({{hora}}) foge do comum. Confirme com o convidado se não houve erro de digitação.",
      "check.past": "A data de gravação informada ({{data}}) já passou. Confirme a data com o convidado.",
      "check.whatsapp_mismatch": "O WhatsApp informado termina em {{agora}}, mas o anotado no convite termina em {{antes}}. Confirme qual está certo.",
      "whatsapp": "O número de WhatsApp informado não foi reconhecido{{end}}. Confirme o número com o convidado.",
      "whatsapp_end": " (termina em {{digits}})",
      "accessibility": "O convidado escreveu algo sobre acessibilidade, mas não marcou a autorização para esse tipo de dado. Pela LGPD, a informação foi descartada. Se for importante para a gravação, pergunte diretamente a ele.",
      "sensitive": "Uma informação pessoal sensível foi descartada porque o convidado não marcou a autorização específica (LGPD).",
      "scheduled_at": "A data de gravação informada não pôde ser lida. Confirme a data com o convidado.",
      "previous_interviews": "No campo de entrevistas anteriores havia uma resposta que não era link; ela foi ignorada.",
      "links": "Um dos links informados não era um endereço válido e foi ignorado.",
      "key_ideas": "O convidado mandou mais de 3 ideias principais; ficaram as 3 primeiras.",
      "other": "Uma resposta do campo \"{{field}}\" foi ignorada."
    },
    "held": "Resposta sem código de convite válido: nada foi enviado ao convidado. Se foi você quem convidou, confirme pelo menu ou com confirmarIntake."
  },
  "sheet": {
    "tab": "Convidados",
    "columns": [
      "Respondeu em",
      "Nome",
      "Como prefere ser chamado(a)",
      "Cargo / atuação",
      "Apresentação",
      "Ideias principais",
      "Quer divulgar",
      "Aceita debater",
      "Prefere não abordar",
      "Gravação",
      "Modalidade",
      "E-mail",
      "WhatsApp",
      "Contato preferido",
      "Revisão antes de publicar",
      "O que já foi enviado",
      "Precisa de atenção",
      "Briefing",
      "Código do registro"
    ],
    "not_informed": "não informado ou não reconhecido",
    "none": "—",
    "briefing_link": "Abrir o briefing"
  },
  "menu": {
    "forget_yes": "Esquecer {{nome}}",
    "window": {
      "cancel": "Cancelar",
      "not_now": "Agora não",
      "continue": "Continuar",
      "working": "Trabalhando…",
      "failed": "Algo deu errado ao falar com o Google. Feche esta janela e tente de novo.",
      "ok": "Fechar",
      "copy": "Copiar",
      "copied": "Copiado ✓",
      "open": "Abrir"
    },
    "start": {
      "guide": "Guia com imagens, tela por tela:",
      "tab": "Comece aqui",
      "title": "Comece aqui: do zero ao primeiro convite em uns 15 minutos",
      "steps": [
        "Esta é a sua cópia da planilha do PodFácil. Ela é só sua: ninguém mais vê o que você põe aqui.",
        "No chat do Claude, peça: \"configurar meu programa no PodFácil\". Ele faz as perguntas e guarda o perfil do programa.",
        "Aqui na planilha, use o menu PodFácil (lá em cima, ao lado de Ajuda). Plano pago: PodFácil > Ativar licença. Plano grátis: PodFácil > Configurar programa e digite o código que o Claude mostrou. Se o menu não aparecer, recarregue a página.",
        "Na primeira vez, o Google pede autorização e mostra a tela \"O Google não verificou este app\", com o SEU e-mail como desenvolvedor. É esperado: a cópia é sua e o PodFácil roda dentro da sua conta. Clique em Avançado, depois em \"Acessar PodFácil — planilha do programa (não seguro)\" e em Continuar; na lista de permissões, deixe tudo marcado e clique em Continuar. A janela fecha sozinha e, em geral, a opção que você escolheu continua sozinha; se nada aparecer em alguns segundos, clique de novo na opção do menu.",
        "O que o Google pede e o que o PodFácil faz: o Google pede acesso às suas planilhas, formulários e agendas porque não tem uma permissão menor para isso, mas o PodFácil só mexe nesta planilha, no formulário do convidado e nos eventos de gravação que ele cria; no Drive, só nos arquivos que ele mesmo cria. Ele também envia e-mails em seu nome (convites e avisos), confere a sua licença no servidor do PodFácil e roda sozinho uma vez por dia (lembretes e fila de convites). Ele não lê seus e-mails.",
        "Com o programa configurado, o PodFácil cria o formulário do convidado. Depois, na aba Convites, escreva uma linha por convidado (nome e e-mail bastam) e use PodFácil > Convidar.",
        "Quando o convidado responder, chega um aviso no seu e-mail e a resposta aparece na aba Convidados."
      ],
      "footer": "Dúvida ou algo estranho? Use PodFácil > Verificar instalação ou pergunte ao Claude no chat."
    },
    "invite": "Convidar (aba Convites)",
    "confirm_guest": "Enviar confirmação ao convidado selecionado",
    "invites": {
      "wait": "Conferindo a aba Convites…",
      "send_button": "Enviar {{n}} convite(s)",
      "wait_send": "Enviando os convites…",
      "busy": "A fila de convites já está rodando agora. Espere uns minutos e veja a coluna Situação.",
      "tab": "Convites",
      "columns": [
        "Nome",
        "E-mail",
        "Data e hora",
        "Modalidade",
        "Link da sala (remota)",
        "WhatsApp (opcional)",
        "Situação"
      ],
      "note": "Uma linha por convidado: nome e e-mail bastam; data, modalidade, link e WhatsApp quando souber. Depois use PodFácil > Convidar. A coluna Situação é preenchida pelo PodFácil.",
      "created": "Criei a aba {{aba}}. Preencha uma linha por convidado (nome e e-mail bastam) e use PodFácil > Convidar de novo.",
      "nothing": "Nenhum convite pendente na aba {{aba}}. Linhas com ✅ ou ➖ já foram tratadas: a mesma pessoa não recebe duas vezes o convite para a mesma data.",
      "confirm": "Enviar {{n}} convite(s) agora?",
      "done": "Pronto.",
      "done_lines": {
        "enviados": "✅ Convites enviados: {{n}}",
        "pulados": "➖ Já tinham recebido (não reenviado): {{n}}",
        "corrigir": "❌ Para corrigir (veja a coluna Situação): {{n}}",
        "falhas": "⚠️ Com falha (use Convidar de novo): {{n}}",
        "depois": "⏳ Ficaram para depois: {{n}}"
      },
      "later": "Os que ficaram para depois saem sozinhos amanhã, no horário do lembrete diário.",
      "need_form": "Antes de convidar, o programa precisa estar configurado e o formulário criado. Use PodFácil > Verificar instalação.",
      "status": {
        "unsure": "⚠️ Sem confirmação de envio (a rodada foi interrompida): confira em Enviados no Gmail; se não saiu, use Convidar de novo",
        "sent": "✅ Enviado em {{quando}}",
        "sent_logo": "✅ Enviado em {{quando}}, sem o logo (use PodFácil > Enviar logo)",
        "already": "➖ Já tinha sido enviado",
        "optout": "➖ Não enviado: a pessoa pediu para não receber",
        "quota": "⏳ Na fila: a cota de e-mails de hoje acabou; sai amanhã",
        "time": "⏳ Na fila: sai na próxima rodada",
        "failed": "⚠️ Falhou: {{motivo}}. Use Convidar de novo para tentar outra vez",
        "fix": "❌ Corrija: {{motivo}}"
      },
      "errors": {
        "past": "a data já passou",
        "name": "falta o nome",
        "email": "e-mail inválido",
        "date": "data e hora não reconhecidas (use 20/10/2026 14:30)",
        "mode": "modalidade não reconhecida (use {{modos}})",
        "link": "o link da sala precisa começar com https://",
        "whatsapp": "WhatsApp não reconhecido (use DDD + número)"
      },
      "digest_subject": "Fila de convites: {{enviados}} enviado(s) hoje",
      "digest_body": "A fila de convites rodou sozinha hoje. Enviados: {{enviados}} · para corrigir: {{corrigir}} · com falha: {{falhas}} · ainda na fila: {{depois}}. Veja a aba {{aba}}: {{url}}"
    },
    "confirm": {
      "send_button": "Enviar a confirmação",
      "wait": "Enviando…",
      "busy": "Essa confirmação já está saindo; não precisa clicar de novo.",
      "held": "Esta resposta está retida (chegou sem código de convite válido). Confirme o convidado antes de enviar e-mail a ele.",
      "title": "Enviar confirmação",
      "ask": "Enviar a {{nome}} um e-mail pedindo para confirmar {{n}} ponto(s)?\n\n{{itens}}",
      "ask_none": "Não achei nada a corrigir nas respostas de {{nome}}. Enviar mesmo assim um e-mail para a pessoa confirmar os dados?",
      "again": "Já foi enviada uma confirmação em {{quando}}.",
      "done": "Confirmação enviada para {{nome}}. A resposta chega no seu e-mail.",
      "optout": "{{nome}} pediu para não receber e-mails do programa; nada foi enviado.",
      "quota": "A cota de e-mails de hoje acabou. Tente de novo amanhã.",
      "not_found": "Não achei as respostas desse convidado (código {{id}})."
    },
    "title": "PodFácil",
    "activate_license": "Ativar licença",
    "check_install": "Verificar instalação",
    "resend_notice": "Reenviar aviso do convidado selecionado",
    "rebuild_guests": "Refazer aba Convidados",
    "forget_guest": "Esquecer convidado selecionado (LGPD)",
    "release_devices": "Liberar outros dispositivos",
    "ask_code_title": "Qual convidado?",
    "ask_code": "Na aba Convidados, clique na linha do convidado e escolha a opção de novo. Ou cole aqui o código do registro (última coluna):",
    "resend_done": "Aviso reenviado para o seu e-mail.",
    "rebuild_done": "Aba Convidados refeita, com os links de briefing preservados.",
    "forget_confirm": "Esquecer {{nome}}? Apaga as respostas, a linha da aba Convidados e o evento da agenda, e manda o briefing para a lixeira (LGPD). Não dá para desfazer.",
    "forget_done": "Pronto: {{nome}} foi esquecido.",
    "forget_pending": "Falta fazer à mão:",
    "error": "Não deu certo: {{motivo}}",
    "license": {
      "plans": {
        "free": "Grátis",
        "individual_solo": "Individual Solo",
        "individual_duo": "Individual Duo",
        "enterprise_10": "Estúdio, até 10 pessoas",
        "enterprise_20": "Estúdio, até 20 pessoas"
      },
      "upgrade_hint": "Sua licença libera o formulário completo: para trocar o essencial por ele, use Verificar instalação.",
      "ok_stay": "Licença ativada (plano {{plano}}). Copie o que precisar acima e feche esta janela.",
      "ok_read": "Licença ativada (plano {{plano}}). Leia o aviso abaixo e feche esta janela.",
      "title": "Ativar licença do PodFácil",
      "lead": "Cole a chave que chegou no seu e-mail depois da compra. Ela fica guardada só neste projeto e não aparece na tela.",
      "label": "Chave de licença",
      "button": "Ativar",
      "working": "Conferindo com o servidor…",
      "ok": "Licença ativada (plano {{plano}}). Esta janela fecha sozinha.",
      "saved_offline": "Chave guardada. O servidor do PodFácil não respondeu agora; a conferência acontece no próximo uso.",
      "invalid": "Isso não parece uma chave de licença. A chave começa com pgi_ e tem 47 letras, números, - e _. No e-mail, não use clique duplo (ele para no primeiro hífen): selecione arrastando do começo ao fim da chave, copie e cole aqui.",
      "refused": "O servidor recusou a chave: {{motivo}}",
      "free_key": "Essa chave está no plano grátis. As automações são do plano pago.",
      "saved_limit": "Chave guardada. Ela chegou ao limite de computadores: use PodFácil > Liberar outros dispositivos.",
      "offline_keep": "O servidor do PodFácil não respondeu agora e já existe uma chave guardada; ela continua valendo. Tente trocar de novo em alguns minutos.",
      "unknown": "O servidor não reconhece essa chave. Confira se copiou a chave inteira do e-mail.",
      "failed": "Algo deu errado ao falar com o Google. Feche esta janela e tente de novo."
    },
    "check": {
      "wait": "Conferindo a instalação…",
      "form_ask_yes": "Criar o formulário",
      "form_gone_yes": "Criar um novo",
      "upgrade_yes": "Trocar pelo completo",
      "form_gone_ask": "O formulário registrado não abre (apagado ou sem acesso). Criar um novo agora? O link do convidado muda; as respostas já recebidas continuam na planilha.",
      "upgrade_ask": "Sua licença paga libera o formulário completo. Trocar agora? O link do convidado muda: o antigo deixa de aceitar respostas, e as respostas já recebidas continuam na planilha.",
      "form_ask": "Ainda não há formulário do convidado. Criar agora? (leva uns segundos)",
      "phone_ok": "WhatsApp do formulário com validação (número incompleto ou com letra não passa)",
      "title": "Verificar instalação",
      "summary_ok": "Tudo certo com o PodFácil.",
      "summary_fail": "{{n}} ponto(s) precisam de você:",
      "show_ok": "Configuração do programa: {{nome}}.",
      "show_missing": "Falta a configuração do programa (o Claude prepara com você).",
      "form_ok": "Formulário do convidado encontrado.",
      "form_missing": "O formulário ainda não foi criado.",
      "form_gone": "O formulário registrado não abre (apagado ou sem acesso).",
      "triggers_ok": "Envios automáticos ligados.",
      "triggers_fixed": "Envios automáticos estavam desligados e foram religados.",
      "guests_ok": "Aba Convidados no lugar.",
      "guests_fixed": "A aba Convidados não existia e foi criada.",
      "guests_fail": "Não consegui criar a aba Convidados: {{motivo}}",
      "license_none": "Sem licença: plano grátis. Para o plano pago, use PodFácil > Ativar licença.",
      "license_paid": "Licença ativa (plano {{plano}}).",
      "license_offline": "Licença guardada; o servidor não respondeu agora.",
      "license_fail": "Licença com problema: {{motivo}}",
      "triggers_other": "Os envios automáticos foram ligados pela conta {{dono}}. Peça para essa pessoa abrir PodFácil > Verificar instalação.",
      "logo_fail": "O logo do Drive não abre para o PodFácil; os convites saem com o nome do programa no lugar. Envie de novo por PodFácil > Enviar logo.",
      "logo_ok": "Logo do convite no lugar."
    },
    "devices": {
      "confirm_yes": "Liberar os dispositivos",
      "title": "Liberar outros dispositivos",
      "confirm": "Isto desconecta todos os computadores ligados à sua licença; cada um volta a funcionar no próximo uso. Vale 2 vezes por mês. Continuar?",
      "done": "Dispositivos liberados.",
      "no_key": "Ative a licença primeiro (PodFácil > Ativar licença)."
    },
    "config": {
      "tz_label": "Fuso horário das datas",
      "ask_code_button": "Configurar",
      "wait_profile": "Buscando o perfil do programa…",
      "wait_form": "Criando o formulário do convidado no Google Forms. Leva de 1 a 2 minutos: pode deixar esta janela aberta.",
      "form_link": "Link do formulário do convidado",
      "form_busy": "O formulário já está sendo criado em outra janela. Espere um minuto e use Verificar instalação.",
      "form_exists": "O formulário do convidado já existe. Link para o convidado: {{url}}",
      "form_created": "Formulário do convidado criado ({{variante}}). Link para o convidado: {{url}} O link também fica guardado na aba Configuração.",
      "form_fail": "Não consegui criar o formulário: {{motivo}}",
      "variants": {"essencial": "essencial", "completo": "completo"},
      "item": "Configurar programa",
      "ask_code_title": "Código do programa",
      "ask_code": "Digite o código de 15 letras e números que o Claude mostrou no chat (com ou sem os traços):",
      "done": "Programa \"{{nome}}\" configurado. Os dados estão na aba {{aba}}.",
      "tab": "Configuração",
      "note": "Esta aba só mostra a configuração. Para mudar, peça ao Claude no chat e use PodFácil > Configurar programa de novo.",
      "labels": {
        "name": "Programa",
        "tagline": "Frase de apresentação",
        "locale": "Idioma",
        "editorial": "Linha editorial",
        "modes": "Grava em",
        "studio": "Estúdio",
        "address": "Endereço",
        "colors": "Cores",
        "logo": "Logo",
        "controller": "Responsável pelos dados (LGPD)",
        "retention": "Guarda das respostas"
      },
      "retention_days": "{{dias}} dias depois da publicação",
      "imported": "Perfil do programa \"{{nome}}\" importado.",
      "logo_item": "Enviar logo",
      "import_failed": "O perfil do programa chegou, mas não consegui gravá-lo ({{motivo}}). Peça ao Claude para salvar de novo e use PodFácil > Configurar programa.",
      "logo": {
        "title": "Logo do convite",
        "lead": "Escolha o logo do programa (PNG ou JPG, até 1 MB). Ele vai embutido nos convites e fica guardado no seu Google Drive.",
        "button": "Enviar",
        "working": "Enviando…",
        "ok": "Logo guardado. Os próximos convites já saem com ele.",
        "too_big": "O arquivo passa de 1 MB. Diminua a imagem e tente de novo.",
        "bad_type": "Use um arquivo PNG ou JPG.",
        "need_show": "Configure o programa primeiro (PodFácil > Configurar programa).",
        "failed": "Algo deu errado ao enviar o logo. Tente de novo."
      }
    }
  },
  "guest_confirm": {
    "subject": "{{show}}: pode confirmar alguns dados da sua participação?",
    "greeting": "Olá, {{nome}}!",
    "intro": "Obrigado por responder ao formulário do {{show}}. Antes da gravação, queremos confirmar alguns pontos:",
    "intro_none": "Obrigado por responder ao formulário do {{show}}. Antes da gravação, queremos confirmar os dados abaixo.",
    "items": {
      "contacts.whatsapp": "Não conseguimos ler o número de WhatsApp que você informou{{end}}. Qual é o número certo, com DDD?",
      "accessibility": "Você escreveu algo sobre acessibilidade, mas não marcou a autorização para guardarmos esse tipo de informação, então ela não foi registrada. Se quiser que a gente se prepare, responda a este e-mail e combinamos como fazer.",
      "scheduled_at": "Não conseguimos ler a data e o horário da gravação. Quando fica bom para você?",
      "check.time_odd": "O horário que você informou foi {{hora}}. Está certo?",
      "check.past": "A data informada ({{data}}) já passou. Qual é a data certa?",
      "check.whatsapp_mismatch": "O WhatsApp que você informou termina em {{agora}}, mas tínhamos anotado um número que termina em {{antes}}. Qual devemos usar?"
    },
    "end": " (termina em {{digits}})",
    "summary": "O que temos anotado",
    "labels": {
      "recording": "Gravação",
      "whatsapp": "WhatsApp"
    },
    "whatsapp_end": "termina em {{digits}}",
    "closing": "Basta responder a este e-mail com a correção. Se estiver tudo certo, responda \"está certo\".",
    "signature": "Equipe do {{show}}"
  }
}

```


## zh.json

```json
{
  "locale": "zh",
  "needs_native_review": true,
  "text_version": "zh/v0-skeleton",
  "form": {
    "validation": {
      "phone": "请输入带国家代码和区号的号码，例如：+86 138 0013 8000。"
    },
    "title": "[TODO-zh] Guest of {{show.name}}",
    "description_essencial": "[TODO-zh] Takes about 2 minutes. It helps us prepare a good conversation for you, with no surprises.",
    "description_completo": "[TODO-zh] Takes about 8 minutes. Almost everything is optional: skip whatever you prefer.",
    "confirmation": "[TODO-zh] Thank you! If you allowed email, the guest kit is on its way. To send files (PDFs, slides, photos), just reply to that email with attachments.",
    "sections": {
      "about": "[TODO-zh] About you",
      "content": "[TODO-zh] The conversation",
      "logistics": "[TODO-zh] Recording",
      "channels": "[TODO-zh] How we reach you",
      "consent": "[TODO-zh] Your data and this interview",
      "sensitive": "[TODO-zh] Sensitive data (optional)",
      "localization": "[TODO-zh] Other languages (optional)"
    },
    "fields": {
      "guest.full_name": {
        "title": "[TODO-zh] Full name",
        "help": ""
      },
      "guest.preferred_name": {
        "title": "[TODO-zh] What should we call you on air?",
        "help": "[TODO-zh] E.g. Ana, Dr. Ana, Professor Silva."
      },
      "guest.name_pronunciation": {
        "title": "[TODO-zh] How is your name pronounced?",
        "help": "[TODO-zh] Only if we might get it wrong."
      },
      "guest.pronouns": {
        "title": "[TODO-zh] Pronouns",
        "help": "[TODO-zh] Optional. E.g. she/her."
      },
      "guest.role_title": {
        "title": "[TODO-zh] Role or occupation",
        "help": ""
      },
      "guest.photo_url": {
        "title": "[TODO-zh] Link to a photo of you for promotion",
        "help": "[TODO-zh] Optional. A public link (website, LinkedIn, shared Drive)."
      },
      "bio.short": {
        "title": "[TODO-zh] Short bio, up to 2 lines",
        "help": "[TODO-zh] This is what we read in the intro."
      },
      "bio.long": {
        "title": "[TODO-zh] Full bio",
        "help": "[TODO-zh] Optional."
      },
      "links": {
        "title": "[TODO-zh] Your main links",
        "help": "[TODO-zh] Website, profiles, portfolio. One per line. If you have none, leave it blank."
      },
      "social_handles": {
        "title": "[TODO-zh] Handles to tag when we promote",
        "help": "[TODO-zh] One per line, as network: @user (e.g. instagram: @ana)."
      },
      "previous_interviews": {
        "title": "[TODO-zh] Interviews you have given",
        "help": "[TODO-zh] Links, one per line. Helps us avoid repeating questions."
      },
      "key_ideas": {
        "title": "[TODO-zh] Up to 3 ideas you want the audience to take away",
        "help": "[TODO-zh] One per line."
      },
      "stories_to_tell": {
        "title": "[TODO-zh] Stories you like to tell",
        "help": "[TODO-zh] One per line."
      },
      "controversies.accepts": {
        "title": "[TODO-zh] Controversial topics you are happy to discuss",
        "help": "[TODO-zh] One per line."
      },
      "controversies.declines": {
        "title": "[TODO-zh] Controversial topics you would rather avoid",
        "help": "[TODO-zh] One per line."
      },
      "off_limits_topics": {
        "title": "[TODO-zh] Off-limits topics",
        "help": "[TODO-zh] We will not touch these. One per line."
      },
      "wants_to_promote": {
        "title": "[TODO-zh] Anything you want to promote?",
        "help": "[TODO-zh] Book, course, event, project. One per line."
      },
      "dream_questions": {
        "title": "[TODO-zh] Questions you would love to be asked",
        "help": "[TODO-zh] One per line."
      },
      "conflicts_of_interest.details": {
        "title": "[TODO-zh] Conflicts of interest or sponsorships related to the topics",
        "help": "[TODO-zh] Leave blank if none."
      },
      "companion.name": {
        "title": "[TODO-zh] Bringing someone along? Who?",
        "help": "[TODO-zh] Leave blank if coming alone."
      },
      "materials": {
        "title": "[TODO-zh] Supporting materials (links)",
        "help": "[TODO-zh] Talks, books, articles, videos. One link per line. Files: reply to the kit email with attachments."
      },
      "recording_mode": {
        "title": "[TODO-zh] How will we record?",
        "help": ""
      },
      "scheduled_at": {
        "title": "[TODO-zh] Date and time already agreed with us",
        "help": "[TODO-zh] Only if already agreed. Used for the calendar invite and the day-before reminder."
      },
      "wants_prepublication_review": {
        "title": "[TODO-zh] Would you like to see the episode before we publish?",
        "help": ""
      },
      "preferred_channel": {
        "title": "[TODO-zh] Preferred channel to reach you",
        "help": ""
      },
      "contacts.email": {
        "title": "[TODO-zh] Your email",
        "help": ""
      },
      "invite.token": {
        "title": "邀请码",
        "help": "已由您收到的邀请邮件中的链接自动填写，请勿修改。如果为空，也请照常提交：节目方会先与您确认，再发送任何内容。"
      },
      "contacts.whatsapp": {
        "title": "[TODO-zh] Your WhatsApp",
        "help": "[TODO-zh] Optional. With country code, e.g. +44 7700 900123."
      },
      "automation_consents": {
        "title": "[TODO-zh] May we use these channels to send you the kit and reminders?",
        "help": "[TODO-zh] Tick only what you want. Nothing ticked = nothing sent through that channel."
      },
      "image_voice": {
        "title": "[TODO-zh] Image and voice",
        "help": ""
      },
      "consent.general": {
        "title": "[TODO-zh] Consent",
        "help": ""
      },
      "consent.public_research": {
        "title": "[TODO-zh] Research in public sources",
        "help": ""
      },
      "consent.divulgacao": {
        "title": "[TODO-zh] Promotion (optional)",
        "help": ""
      },
      "accessibility.needs": {
        "title": "[TODO-zh] SENSITIVE DATA — Do you need any accessibility accommodation?",
        "help": "[TODO-zh] Optional. It may reveal health information: it is only used if you tick the consent right below."
      },
      "accessibility.accept": {
        "title": "[TODO-zh] SENSITIVE DATA — Specific consent (accessibility)",
        "help": ""
      },
      "sensitive.category": {
        "title": "[TODO-zh] SENSITIVE DATA — What is it about?",
        "help": "[TODO-zh] Optional."
      },
      "sensitive.value": {
        "title": "[TODO-zh] SENSITIVE DATA — What you want us to know",
        "help": "[TODO-zh] Optional. Write only what you want in the preparation."
      },
      "sensitive.accept": {
        "title": "[TODO-zh] SENSITIVE DATA — Specific consent",
        "help": ""
      },
      "localization.translation_text": {
        "title": "[TODO-zh] Translated subtitles and texts",
        "help": ""
      },
      "localization.dub_generic_voice": {
        "title": "[TODO-zh] Dubbing with a generic synthetic voice",
        "help": ""
      },
      "localization.dub_voice_replica": {
        "title": "[TODO-zh] SENSITIVE DATA — Artificial replica of your voice",
        "help": ""
      }
    },
    "choices": {
      "recording_mode": {
        "presencial": "[TODO-zh] In person, at the studio",
        "remoto": "[TODO-zh] Remote, online"
      },
      "yes_no": {
        "yes": "[TODO-zh] Yes",
        "no": "[TODO-zh] No"
      },
      "preferred_channel": {
        "email": "[TODO-zh] Email",
        "whatsapp": "[TODO-zh] WhatsApp",
        "phone": "[TODO-zh] Phone",
        "other": "[TODO-zh] Other"
      },
      "channels": {
        "email": "[TODO-zh] Email: guest kit and a day-before reminder",
        "whatsapp": "[TODO-zh] WhatsApp: kit and a day-before reminder",
        "calendar": "[TODO-zh] Calendar: invite with date and address"
      },
      "sensitive_category": {
        "origem_racial_etnica": "[TODO-zh] Racial or ethnic origin",
        "conviccao_religiosa": "[TODO-zh] Religious belief",
        "opiniao_politica": "[TODO-zh] Political opinion",
        "filiacao_sindical_religiosa_filosofica_politica": "[TODO-zh] Trade union or religious, philosophical or political membership",
        "saude": "[TODO-zh] Health",
        "vida_sexual": "[TODO-zh] Sex life",
        "genetico": "[TODO-zh] Genetic data",
        "biometrico": "[TODO-zh] Biometric data"
      }
    }
  },
  "consent": {
    "contact_email": "[TODO-zh] by email at {{email}}",
    "contact_reply_to_email": "[TODO-zh] by replying to any email from this show (including the invitation or the guest kit)",
    "clauses": {
      "BR-LGPD": {
        "clause_id": "BR-LGPD/v1",
        "legal_review": "pending",
        "text": "[TODO-zh] {{controller.name}} (data controller{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contact: {{controller.contact}}) will use the answers to this form only for the purposes below, related to your interview on {{show.name}}: {{purposes}}.\n\nTo prepare better questions, we will also look at information you have made public yourself (website, social media, interviews and published texts). Everything that goes into the preparation material will cite its source.\n\nWe will not use or keep sensitive data (health, religion, political opinion, sex life, racial or ethnic origin, among others) unless you write it yourself in the optional sensitive-data section and tick the specific consent for each item. It is your decision.\n\nThe data is deleted within {{retention_days}} days after the episode is published; we keep only the record of this consent, as proof. At any time and free of charge you may request access, correction or deletion, or withdraw this consent, {{controller.contact}}. If you do not want to consent, simply do not submit the form: the interview can still happen without it."
      },
      "EU-GDPR": {
        "clause_id": "EU-GDPR/v1",
        "legal_review": "pending",
        "text": "[TODO-zh] {{controller.name}} (data controller{{#controller.document_id}}, {{controller.document_id}}{{/controller.document_id}}; contact: {{controller.contact}}) will process the answers to this form based on your consent, only for: {{purposes}}.\n\nWe will also look at information you have made publicly accessible (website, social media, interviews, published texts), always citing the source.\n\nSpecial categories of data (health, religion, political opinion, sex life, racial or ethnic origin, among others) are processed only if you write them in the optional section and give explicit consent for each item.\n\nThe data is deleted within {{retention_days}} days after the episode is published. You have the right of access, rectification, erasure, restriction, portability and objection, and you may withdraw consent at any time ({{controller.contact}}) without affecting processing already carried out. You may also lodge a complaint with a supervisory authority."
      },
      "other": {
        "clause_id": "other/v1",
        "legal_review": "pending",
        "text": "[TODO-zh] {{controller.name}} (contact: {{controller.contact}}) will use the answers to this form only for: {{purposes}}. We will also look at information you have made public, always citing the source. Sensitive data is used only if you write it in the optional section and tick the specific consent. The data is deleted within {{retention_days}} days after publication. To access, correct, delete or withdraw consent: {{controller.contact}}."
      },
      "CN-PIPL": {
        "clause_id": "CN-PIPL/v0",
        "legal_review": "pending",
        "text": "[TODO-zh] PIPL clause not drafted. Requires separate consent for sensitive personal information (PIPL art. 29) and native legal review before use. {{controller.name}} {{controller.contact}} {{purposes}} {{retention_days}}"
      }
    },
    "purposes": {
      "preparo_entrevista": "[TODO-zh] preparing your interview",
      "dossie": "[TODO-zh] building the preparation material (with sources)",
      "memoria_episodio": "[TODO-zh] recording the episode in the show's archive",
      "divulgacao": "[TODO-zh] promoting the episode with your short bio, photo and handle"
    },
    "draft_notice": "[TODO-zh] NOTICE: this consent text is a DRAFT (v0) under legal review and may change. If the final version changes anything, we will ask for your consent again.",
    "general_accept": "[TODO-zh] I have read the text above and agree to the use of my answers for these purposes.",
    "public_research_accept": "[TODO-zh] I understand that information I have made public myself will be consulted, always citing the source.",
    "divulgacao_accept": "[TODO-zh] I also allow my short bio, photo and handle to be used to promote the episode.",
    "image_voice_accept": "[TODO-zh] I authorise the recording and publication of my image and voice in this episode.",
    "sensitive_intro": "[TODO-zh] This section is entirely optional and the decision is yours. Everything here is SENSITIVE DATA: it is used only if you write it and tick the specific consent right below each field. Without consent the information is discarded and not kept.",
    "sensitive_accept": "[TODO-zh] SENSITIVE DATA — I give specific, explicit consent to the use of the information I wrote above only to prepare and conduct this interview.",
    "accessibility_accept": "[TODO-zh] SENSITIVE DATA (may reveal health) — I allow the accessibility need above to be used only to organise the recording logistics.",
    "sensitive_purpose": "[TODO-zh] prepare and conduct this interview",
    "accessibility_purpose": "[TODO-zh] organise the recording logistics",
    "localization_intro": "[TODO-zh] This section is optional and each permission is separate: tick only what you want. None of them is a condition for the interview, and none comes pre-ticked. You can withdraw any of them at any time, free of charge, through the same contact given in the data section.",
    "translation_accept": "[TODO-zh] I allow my speech to be transcribed and translated subtitles and texts of this episode (including the description) to be published in: {{locales}}.",
    "dub_generic_accept": "[TODO-zh] I allow a dubbed version of this episode with a generic synthetic voice (not my voice), speaking the translation of my words, disclosed to the audience as AI dubbing, in: {{locales}}.",
    "dub_replica_accept": "[TODO-zh] SENSITIVE DATA — I give specific, explicit consent to the creation of an artificial replica of my voice solely to dub THIS episode in {{locales}}, by the provider {{provider}} ({{country}}), with my voice model deleted within {{days}} days after dubbing. The dubbed version will be disclosed to the audience as AI-made. I can withdraw at any time.",
    "dub_replica_purpose": "[TODO-zh] dub this episode with an artificial replica of the data subject's voice"
  },
  "kit": {
    "title": "[TODO-zh] Guest kit",
    "greeting": "[TODO-zh] Hello, {{guest.preferred_name}}!",
    "thanks": "[TODO-zh] We are glad to have you on {{show.name}}. This kit gathers what you need to know before the recording. Read it calmly, whenever you can.",
    "about_heading": "[TODO-zh] What {{show.name}} is",
    "pillars_heading": "[TODO-zh] The topics we cover",
    "when_heading": "[TODO-zh] When",
    "when_tbd": "[TODO-zh] The date is still to be agreed with the production team.",
    "where_heading": "[TODO-zh] Where (in-person recording)",
    "address_label": "[TODO-zh] Address",
    "landmarks_label": "[TODO-zh] Landmarks",
    "gps_label": "[TODO-zh] In your GPS or ride app, type",
    "parking_label": "[TODO-zh] Parking",
    "arrive": "[TODO-zh] Please arrive {{arrive.min}} to {{arrive.max}} minutes early, to have some water and test the sound without rushing.",
    "remote_heading": "[TODO-zh] Remote recording: what you need",
    "remote_default": [
      "[TODO-zh] Headphones (wired, if you have them)",
      "[TODO-zh] A quiet room with little echo",
      "[TODO-zh] A stable connection; cable rather than Wi-Fi if possible",
      "[TODO-zh] Computer charged or plugged in"
    ],
    "conduct_heading": "[TODO-zh] So you can feel at ease",
    "conduct_default": [
      "[TODO-zh] There are no wrong answers: it is a conversation, not an exam.",
      "[TODO-zh] If you stumble or want to redo an answer, just say so. We edit.",
      "[TODO-zh] You can ask not to discuss a topic at any moment.",
      "[TODO-zh] Water whenever you like, and breaks too."
    ],
    "materials_heading": "[TODO-zh] Materials (optional)",
    "materials_text": "[TODO-zh] Want to send slides, PDFs, photos or links? Reply to this email with attachments. No account needed anywhere.",
    "privacy_heading": "[TODO-zh] Your data",
    "privacy_text": "[TODO-zh] We use your answers only to prepare this interview. To access, correct, delete or withdraw consent: {{controller.contact}}.",
    "signoff": "[TODO-zh] See you soon!",
    "parking": {
      "disponivel": "[TODO-zh] available on site",
      "indisponivel": "[TODO-zh] no parking on site",
      "pago_proximo": "[TODO-zh] paid parking nearby",
      "pendente": "[TODO-zh] to be confirmed by the production team"
    }
  },
  "messages": {
    "email_subject": "[TODO-zh] Guest kit · {{show.name}}",
    "owner_subject": "✅ {{guest.preferred_name}} 已填写表单 · {{show.name}}",
    "calendar_title": "[TODO-zh] {{show.name}} recording with {{guest.preferred_name}}",
    "calendar_remote_location": "[TODO-zh] Online (link from the production team)",
    "calendar_description": "[TODO-zh] Guest kit sent by email. Questions: {{controller.contact}}.",
    "whatsapp_kit": "[TODO-zh] Hello, {{guest.preferred_name}}! This is {{show.name}}. We got your form, thank you! The guest kit with all the details is in your email.{{#address_line}} Address: {{address_line}}.{{/address_line}}{{#gps_hint}} In your GPS, type: {{gps_hint}}.{{/gps_hint}}",
    "reminder_subject": "[TODO-zh] Tomorrow: recording at {{show.name}}",
    "reminder_body": "[TODO-zh] Hello, {{guest.preferred_name}}! Reminder: the {{show.name}} recording is tomorrow, {{scheduled_text}}.{{#address_line}} Address: {{address_line}}.{{/address_line}}{{#gps_hint}} In your GPS, type: {{gps_hint}}.{{/gps_hint}}{{#arrive}} Please arrive {{arrive.min}} to {{arrive.max}} minutes early.{{/arrive}} Any questions, just reply."
  },
  "_note": "ESQUELETO: textos copiados do en e marcados [TODO-zh]. Precisa de tradução e revisão nativa (e jurídica) antes de uso. O build do formulário recusa este locale enquanto needs_native_review=true, salvo ALLOW_UNREVIEWED_LOCALE=true.",
  "invitation": {
    "subject": "[TODO-zh] Official invitation · {{show.name}}",
    "preheader": "[TODO-zh] {{show.name}} invites you to a conversation. Date, place and form inside.",
    "title": "[TODO-zh] Official invitation",
    "greeting": "[TODO-zh] Hello, {{guest.name}}!",
    "intro": {
      "formal": "[TODO-zh] We are honored to invite you to be a guest on {{show.name}}.",
      "cordial": "[TODO-zh] It is a pleasure to invite you for a conversation on {{show.name}}.",
      "descontraido": "[TODO-zh] Let's record? We'd love to have you on {{show.name}}."
    },
    "when_label": "[TODO-zh] Date and time",
    "when_tbd": "[TODO-zh] to be agreed with the production team",
    "where_label": "[TODO-zh] Place",
    "gps_label": "[TODO-zh] In your GPS or ride app, type",
    "arrival_label": "[TODO-zh] How to get there",
    "arrive": "[TODO-zh] Please arrive {{arrive.min}} to {{arrive.max}} minutes early.",
    "remote_label": "[TODO-zh] Remote recording, room link",
    "remote_link_tbd": "[TODO-zh] the room link will arrive by e-mail before the recording",
    "about_heading": "[TODO-zh] What {{show.name}} is",
    "cta_intro": {
      "essencial": "[TODO-zh] So we can prepare a conversation worthy of you, please fill in the guest form. It takes about 2 minutes.",
      "completo": "[TODO-zh] So we can prepare a conversation worthy of you, please fill in the guest form. It takes about 8 minutes, and almost everything is optional."
    },
    "cta_button": "[TODO-zh] Fill in the form",
    "cta_fallback": "[TODO-zh] If the button does not open, copy and paste this address into your browser:",
    "signoff": "[TODO-zh] Kind regards,",
    "footer_controller": "[TODO-zh] Sent by: {{controller.name}}, data controller. Contact: {{controller.contact}}.",
    "footer_purpose": "[TODO-zh] You received this invitation because {{signature.name}} suggested you as a guest. We use your name and e-mail only for this invitation and to organize the interview; the guest kit arrives after you answer the form.",
    "footer_optout": "[TODO-zh] Don't want to hear from {{show.name}} again? Reply to this e-mail with the word STOP and we will not send anything else.",
    "footer_brand": "[TODO-zh] Prepared with PodFácil",
    "ics_description": "[TODO-zh] Official invitation from {{show.name}}. Guest form: {{form_url}}"
  },
  "decision": {
    "ack": {
      "v1": "[TODO-zh] I have read the alerts above. I understand the plugin only recommends: the decision to go against the recommendation is mine, and the editorial and legal responsibility for what is recorded and published is mine (or of whom I represent), not the plugin's nor its authors'."
    },
    "alerts": {
      "R-CLAIM-CONDUTA-FONTES": "[TODO-zh] This statement about someone's conduct lacks the recommended backing (verified status with 1 primary source or 2 independent press sources). Using it on air may create defamation liability.",
      "R-CLAIM-CONDUTA-INDEPENDENCIA": "[TODO-zh] The press sources for this conduct statement may not be independent (same domain, author or agency). Check author, outlet and agency before deciding.",
      "R-ROTEIRO-GATE-PENDENTE": "[TODO-zh] The @guardian review (fact-check) has not been done yet for a mode that recommends it before recording.",
      "R-ROTEIRO-GATE-AJUSTES": "[TODO-zh] The @guardian recommended adjustments that are not recorded as applied.",
      "R-ROTEIRO-GATE-VETADO": "[TODO-zh] The @guardian recommended NOT recording this script as is. Recording against that recommendation is your decision and your responsibility.",
      "R-ROTEIRO-CONTRADITORIO": "[TODO-zh] This mode recommends hearing the named party before recording, and no right-of-reply request is recorded.",
      "R-ROTEIRO-REVISAO-JURIDICA": "[TODO-zh] This mode carries high legal risk and the recommended human legal review is still pending.",
      "R-ROTEIRO-SEM-LASTRO": "[TODO-zh] Some factual statements have no dossier claim nor source. Saying unbacked things on air is your editorial risk.",
      "R-ROTEIRO-INFERENCIA-COMO-FATO": "[TODO-zh] An inference (hypothesis) appears as a factual statement. The recommendation is to turn it into a question or hypothesis.",
      "R-ROTEIRO-RIGOR": "[TODO-zh] The mode asks for sources for numbers, dates and quotes, and this statement rests only on self-declared information.",
      "R-ROTEIRO-DEGRADADO": "[TODO-zh] The dossier is incomplete and this block uses its statements without a caveat to confirm with the guest.",
      "R-ROTEIRO-TIMING": "[TODO-zh] The sum of block durations is more than 15% away from the target duration.",
      "R-FACTCHECK-SEM-FONTE": "[TODO-zh] The fact-check found no source for this statement.",
      "R-FACTCHECK-DISCLOSURE": "[TODO-zh] The recommended advertising or sponsorship disclosure is missing.",
      "R-FACTCHECK-LGPD": "[TODO-zh] Third-party personal data is cited without a clear legal basis. (Sensitive data not self-declared is not an alert: it is forbidden.)",
      "R-PUBLICACAO-GATE": "[TODO-zh] The episode quality gate did not recommend publication (REQUEST CHANGES or HOLD).",
      "R-MEMORIA-ROTEIRO-PENDENTE": "[TODO-zh] No script linked to this episode is ready to record (pronto_para_gravar). Recording anyway is your decision and responsibility.",
      "R-LOCALIZACAO-REVISAO-HUMANA": "[TODO-zh] Machine translation: review source and translation side by side (names, numbers, glossary terms) before publishing.",
      "R-LOCALIZACAO-SEM-ACEITE-TRADUCAO": "[TODO-zh] There is no recorded guest consent for translated subtitles and texts in this language. Publishing anyway is your decision and responsibility.",
      "R-LOCALIZACAO-SEM-ACEITE-VOZ-GENERICA": "[TODO-zh] There is no recorded guest consent for dubbing with a generic synthetic voice in this language. Publishing anyway is your decision and responsibility.",
      "R-LOCALIZACAO-AGENTE-POLITICO": "[TODO-zh] The guest is flagged as a candidate or political figure. Synthetic content with candidates' voices is subject to electoral rules in Brazil (TSE Resolution 23.732/2024; secondary source, check the current text): verify the electoral calendar and labelling before publishing the dub.",
      "R-LOCALIZACAO-GLOSSARIO": "[TODO-zh] Show glossary terms do not appear as expected in the translation (proper name, acronym or do-not-translate term).",
      "R-LOCALIZACAO-NUMEROS": "[TODO-zh] Some numbers from the source (dates, rates, statute articles) do not appear in the translation.",
      "R-LOCALIZACAO-CPS": "[TODO-zh] Some subtitles exceed the reading-speed limit (characters per second)."
    }
  },
  "localization": {
    "language_names": {
      "pt-BR": "葡萄牙语",
      "en": "英语",
      "es": "西班牙语",
      "zh": "中文"
    },
    "disclosure": {
      "subtitles": "[TODO-zh] Machine translation reviewed by {{show}}.",
      "dub_generic": "本集为基于{{source_language}}原版节目的AI配音版本，声音为合成语音。",
      "dub_replica": "本集为基于{{source_language}}原版节目的AI配音版本，经授权使用AI复制的说话者声音。"
    }
  },
  "owner": {
    "failed": {
      "subject": "PodFácil：有一条表单回复未能处理",
      "body": "嘉宾表单在 {{quando}} 收到一条回复，但 PodFácil 未能处理。\n\n原因：{{motivo}}\n\n嘉宾可能尚未收到资料包或日历邀请。回复已保存在你表格的“表单回复”标签页中。请把这封邮件给聊天中的 Claude 看，以便解决。"
    },
    "confirm_hint": "如需请嘉宾更正：在嘉宾标签页中点击该嘉宾所在的行，然后使用 PodFácil > 发送确认。",
    "headline": "{{name}} 已填写表单。",
    "lead": "所有信息均已记录。以下是目前已完成的事项以及嘉宾提供的信息。",
    "happened": "已完成事项",
    "form_received": "已收到邀请并填写表单",
    "attention": "需要你关注",
    "summary": "嘉宾概要",
    "button": "查看完整回答",
    "next_step": "下一步：请让 Claude\"为 {{name}} 准备简报\"，以获取档案和访谈提纲。",
    "notes": "备注",
    "record_code": "记录编号：{{id}}",
    "full_answers": "完整回答：{{url}}",
    "labels": {
      "name": "姓名",
      "prefers": "希望被称为 {{name}}",
      "role": "职位",
      "bio": "简介",
      "ideas": "核心观点",
      "recording": "录制",
      "email": "电子邮件",
      "whatsapp": "WhatsApp"
    },
    "mode": {
      "presencial": "现场",
      "remoto": "远程"
    },
    "date_tbd": "待定",
    "sends": {
      "kit_email": "嘉宾资料包（电子邮件）",
      "kit_whatsapp": "嘉宾资料包（WhatsApp）",
      "calendar": "日历邀请",
      "automations": "自动发送（资料包和日历）", "guest": "发送给嘉宾",
      "other": "发送\"{{key}}\""
    },
    "status": {
      "sent": "{{label}}：已发送",
      "skipped": "{{label}}：未发送",
      "off": "{{label}}：此表格未启用 WhatsApp",
      "error": "{{label}}：失败",
      "held": "{{label}}：等待你的确认"
    },
    "drops": {
      "check.time_odd": "填写的时间（{{hora}}）不太常见。请与嘉宾确认是否输入有误。",
      "check.past": "填写的录制日期（{{data}}）已经过去。请与嘉宾确认日期。",
      "check.whatsapp_mismatch": "填写的 WhatsApp 号码尾号为 {{agora}}，但邀请中记录的号码尾号为 {{antes}}。请确认哪个正确。",
      "whatsapp": "无法识别所填写的 WhatsApp 号码{{end}}。请与嘉宾确认号码。",
      "whatsapp_end": "（尾号 {{digits}}）",
      "accessibility": "嘉宾填写了无障碍需求，但未勾选此类数据的授权，因此该信息已被删除。如对录制很重要，请直接询问嘉宾。",
      "sensitive": "由于嘉宾未勾选专门授权，一项敏感个人信息已被删除。",
      "scheduled_at": "无法读取录制日期。请与嘉宾确认日期。",
      "previous_interviews": "\"以往采访\"一栏中有一项不是链接，已忽略。",
      "links": "其中一个链接不是有效地址，已忽略。",
      "key_ideas": "嘉宾提交了超过 3 个核心观点，仅保留前 3 个。",
      "other": "\"{{field}}\"栏中的一项回答已忽略。"
    },
    "held": "回答没有有效的邀请码：未向嘉宾发送任何内容。如果是你邀请的，请通过菜单或 confirmarIntake 确认。"
  },
  "sheet": {
    "tab": "嘉宾",
    "columns": [
      "回答时间",
      "姓名",
      "希望的称呼",
      "职位",
      "简介",
      "核心观点",
      "希望推广",
      "愿意讨论",
      "希望避免",
      "录制",
      "形式",
      "电子邮件",
      "WhatsApp",
      "首选联系方式",
      "发布前审阅",
      "已发送内容",
      "需要关注",
      "简报",
      "记录编号"
    ],
    "not_informed": "未提供或无法识别",
    "none": "—",
    "briefing_link": "打开简报"
  },
  "menu": {
    "forget_yes": "删除 {{nome}} 的数据",
    "window": {
      "cancel": "取消",
      "not_now": "暂不",
      "continue": "继续",
      "working": "处理中…",
      "failed": "与 Google 通信时出错。请关闭此窗口后重试。",
      "ok": "关闭",
      "copy": "复制",
      "copied": "已复制 ✓",
      "open": "打开"
    },
    "start": {
      "guide": "图文指南，逐屏说明（英文）：",
      "tab": "从这里开始",
      "title": "从这里开始：大约 15 分钟，从零到发出第一份邀请",
      "steps": [
        "这是你的 PodFácil 表格副本，只属于你：别人看不到你在这里填写的内容。",
        "在 Claude 聊天中说：“在 PodFácil 中设置我的节目”。Claude 会提问并保存节目资料。",
        "在这个表格里使用 PodFácil 菜单（在顶部“帮助”旁边）。付费版：PodFácil > 激活许可证。免费版：PodFácil > 配置节目，并输入 Claude 显示的代码。如果看不到菜单，请刷新页面。",
        "第一次使用时，Google 会请求授权并显示“Google 尚未验证此应用”的页面，开发者一栏显示的是你自己的邮箱。这是正常的：副本属于你，PodFácil 在你自己的账号里运行。点击“高级”，再点击“转至 PodFácil — planilha do programa（不安全）”和“继续”；在权限列表中保持全部勾选，然后点击“继续”。窗口会自动关闭，你选择的选项通常会自动继续；如果几秒钟后没有任何反应，请再次点击该菜单选项。",
        "Google 请求的权限与 PodFácil 实际所做的事：Google 会请求访问你的表格、表单和日历，因为它没有更小范围的权限可选；但 PodFácil 只处理这个表格、嘉宾表单和它自己创建的录制活动；在云端硬盘中只处理它自己创建的文件。它还会以你的名义发送邮件（邀请和通知），在 PodFácil 服务器上核验你的许可证，并且每天自动运行一次（提醒和邀请队列）。它不会读取你的邮件。",
        "节目配置完成后，PodFácil 会创建嘉宾表单。然后在“邀请”标签页中，每位嘉宾填写一行（姓名和电子邮件即可），并使用 PodFácil > 发送邀请。",
        "嘉宾回复后，你的邮箱会收到通知，回答会出现在“嘉宾”标签页中。"
      ],
      "footer": "有疑问或发现异常？请使用 PodFácil > 检查安装，或在聊天中询问 Claude。"
    },
    "invite": "发送邀请（邀请标签页）",
    "confirm_guest": "向所选嘉宾发送确认",
    "invites": {
      "wait": "正在检查“邀请”标签页…",
      "send_button": "发送 {{n}} 份邀请",
      "wait_send": "正在发送邀请…",
      "busy": "邀请队列正在运行。请稍等几分钟，再查看状态列。",
      "tab": "邀请",
      "columns": [
        "姓名",
        "电子邮件",
        "日期和时间",
        "录制方式",
        "会议室链接（远程）",
        "WhatsApp（可选）",
        "状态"
      ],
      "note": "每位嘉宾一行：填写姓名和电子邮件即可；日期、录制方式、链接和 WhatsApp 知道时再填。然后使用 PodFácil > 发送邀请。状态列由 PodFácil 填写。",
      "created": "已创建 {{aba}} 标签页。请每位嘉宾填写一行（姓名和电子邮件即可），然后再次使用 PodFácil > 发送邀请。",
      "nothing": "{{aba}} 标签页中没有待发送的邀请。带 ✅ 或 ➖ 的行已处理：同一个人不会在同一日期收到两次邀请。",
      "confirm": "现在发送 {{n}} 份邀请吗？",
      "done": "完成。",
      "done_lines": {
        "enviados": "✅ 已发送邀请：{{n}}",
        "pulados": "➖ 之前已收到（未重发）：{{n}}",
        "corrigir": "❌ 需要修改（见“状态”列）：{{n}}",
        "falhas": "⚠️ 发送失败（请再次使用“邀请”）：{{n}}",
        "depois": "⏳ 稍后处理：{{n}}"
      },
      "later": "稍后发送的邀请会在明天每日提醒的时间自动发出。",
      "need_form": "发送邀请前，需要先配置节目并创建表单。请使用 PodFácil > 检查安装。",
      "status": {
        "unsure": "⚠️ 无法确认是否已发送（本轮被中断）：请在 Gmail 的已发送中查看；如未发出，请再次使用发送邀请",
        "sent": "✅ 已于 {{quando}} 发送",
        "sent_logo": "✅ 已于 {{quando}} 发送，未附标志（请使用 PodFácil > 上传标志）",
        "already": "➖ 之前已发送",
        "optout": "➖ 未发送：对方要求不再接收邮件",
        "quota": "⏳ 排队中：今日邮件配额已用完；明天发送",
        "time": "⏳ 排队中：下一轮发送",
        "failed": "⚠️ 失败：{{motivo}}。再次使用发送邀请可重试",
        "fix": "❌ 请更正：{{motivo}}"
      },
      "errors": {
        "past": "日期已经过去",
        "name": "缺少姓名",
        "email": "电子邮件无效",
        "date": "无法识别日期和时间（请使用 2026-10-20 14:30）",
        "mode": "无法识别录制方式（请使用 {{modos}}）",
        "link": "会议室链接必须以 https:// 开头",
        "whatsapp": "无法识别 WhatsApp 号码（请使用 +国家代码和号码）"
      },
      "digest_subject": "邀请队列：今天已发送 {{enviados}} 份",
      "digest_body": "邀请队列今天已自动运行。已发送：{{enviados}} · 需更正：{{corrigir}} · 失败：{{falhas}} · 仍在排队：{{depois}}。请查看 {{aba}} 标签页：{{url}}"
    },
    "confirm": {
      "send_button": "发送确认",
      "wait": "正在发送…",
      "busy": "此确认正在发送中，无需再次点击。",
      "held": "此回答已被暂扣（提交时没有有效的邀请码）。请先确认这位嘉宾，再给其发送邮件。",
      "title": "发送确认",
      "ask": "向 {{nome}} 发送邮件，请其确认 {{n}} 项内容吗？\n\n{{itens}}",
      "ask_none": "在 {{nome}} 的回答中没有发现需要更正的内容。仍然发送邮件请其确认资料吗？",
      "again": "已于 {{quando}} 发送过确认。",
      "done": "已向 {{nome}} 发送确认。回复会发到你的邮箱。",
      "optout": "{{nome}} 要求不再接收节目的邮件；未发送任何内容。",
      "quota": "今日邮件配额已用完。请明天再试。",
      "not_found": "找不到这位嘉宾的回答（编号 {{id}}）。"
    },
    "title": "PodFácil",
    "activate_license": "激活许可证",
    "check_install": "检查安装",
    "resend_notice": "重新发送所选嘉宾的通知",
    "rebuild_guests": "重建嘉宾标签页",
    "forget_guest": "删除所选嘉宾的数据（隐私）",
    "release_devices": "释放其他设备",
    "ask_code_title": "哪位嘉宾？",
    "ask_code": "在嘉宾标签页中点击该嘉宾所在的行，然后再次选择此选项。或在此粘贴记录编号（最后一列）：",
    "resend_done": "通知已重新发送到你的邮箱。",
    "rebuild_done": "嘉宾标签页已重建，简报链接已保留。",
    "forget_confirm": "删除 {{nome}} 的数据？这会删除回答、嘉宾行和日历事件，并把简报移到回收站。此操作无法撤销。",
    "forget_done": "完成：已删除 {{nome}} 的数据。",
    "forget_pending": "仍需手动处理：",
    "error": "未成功：{{motivo}}",
    "license": {
      "plans": {
        "free": "免费",
        "individual_solo": "个人单设备",
        "individual_duo": "个人双设备",
        "enterprise_10": "工作室（最多 10 人）",
        "enterprise_20": "工作室（最多 20 人）"
      },
      "upgrade_hint": "你的许可证解锁了完整表单：要用它替换基础表单，请使用“检查安装”。",
      "ok_stay": "许可证已激活（{{plano}} 方案）。请复制上面需要的内容，然后关闭此窗口。",
      "ok_read": "许可证已激活（{{plano}} 方案）。请阅读下面的提示，然后关闭此窗口。",
      "title": "激活 PodFácil 许可证",
      "lead": "粘贴购买后通过邮件收到的密钥。它只保存在此项目中，不会显示在屏幕上。",
      "label": "许可证密钥",
      "button": "激活",
      "working": "正在向服务器确认…",
      "ok": "许可证已激活（{{plano}} 方案）。此窗口会自动关闭。",
      "saved_offline": "密钥已保存。PodFácil 服务器暂未响应，将在下次使用时确认。",
      "invalid": "这看起来不像许可证密钥。密钥以 pgi_ 开头，共 47 个字符（字母、数字、- 和 _）。在邮件中不要双击（双击会在第一个连字符处停止）：请从密钥开头拖动到结尾选中，复制后粘贴到这里。",
      "refused": "服务器拒绝了该密钥：{{motivo}}",
      "free_key": "该密钥属于免费方案。自动化功能属于付费方案。",
      "saved_limit": "密钥已保存。它已达到电脑数量上限：请使用 PodFácil > 释放其他设备。",
      "offline_keep": "PodFácil 服务器暂未响应，且已保存了一个密钥；该密钥继续有效。请几分钟后再尝试更换。",
      "unknown": "服务器无法识别该密钥。请确认已从邮件中完整复制密钥。",
      "failed": "与 Google 通信时出错。请关闭此窗口后重试。"
    },
    "check": {
      "wait": "正在检查安装…",
      "form_ask_yes": "创建表单",
      "form_gone_yes": "新建一个",
      "upgrade_yes": "更换为完整表单",
      "form_gone_ask": "已登记的表单无法打开（已删除或无权限）。现在新建一个吗？嘉宾链接会改变；已收到的回复仍保留在表格中。",
      "upgrade_ask": "你的付费许可证解锁了完整表单。现在更换吗？嘉宾链接会改变：旧链接不再接受回复，已收到的回复仍保留在表格中。",
      "form_ask": "还没有嘉宾表单。现在创建吗？（需要几秒钟）",
      "phone_ok": "表单中的 WhatsApp 字段已启用校验（号码不完整或含字母都无法提交）",
      "title": "检查安装",
      "summary_ok": "PodFácil 一切正常。",
      "summary_fail": "有 {{n}} 项需要你处理：",
      "show_ok": "节目设置：{{nome}}。",
      "show_missing": "缺少节目设置（Claude 会和你一起准备）。",
      "form_ok": "已找到嘉宾表单。",
      "form_missing": "表单尚未创建。",
      "form_gone": "已登记的表单无法打开（已删除或无权限）。",
      "triggers_ok": "自动发送已开启。",
      "triggers_fixed": "自动发送原本已关闭，现已重新开启。",
      "guests_ok": "嘉宾标签页已就位。",
      "guests_fixed": "嘉宾标签页不存在，现已创建。",
      "guests_fail": "无法创建嘉宾标签页：{{motivo}}",
      "license_none": "没有许可证：免费方案。如需付费方案，请使用 PodFácil > 激活许可证。",
      "license_paid": "许可证有效（{{plano}} 方案）。",
      "license_offline": "许可证已保存；服务器暂未响应。",
      "license_fail": "许可证有问题：{{motivo}}",
      "triggers_other": "自动发送是由账户 {{dono}} 开启的。请让此人打开 PodFácil > 检查安装。",
      "logo_fail": "PodFácil 无法打开云端硬盘中的标志；邀请函会改用节目名称。请通过 PodFácil > 上传标志重新上传。",
      "logo_ok": "邀请函标志已就位。"
    },
    "devices": {
      "confirm_yes": "释放设备",
      "title": "释放其他设备",
      "confirm": "这会断开与你的许可证关联的所有电脑；每台电脑在下次使用时会重新生效。每月可使用 2 次。继续吗？",
      "done": "设备已释放。",
      "no_key": "请先激活许可证（PodFácil > 激活许可证）。"
    },
    "config": {
      "tz_label": "日期所用时区",
      "ask_code_button": "设置",
      "wait_profile": "正在获取节目资料…",
      "wait_form": "正在 Google 表单中创建嘉宾表单，需要 1 到 2 分钟：可以让此窗口保持打开。",
      "form_link": "嘉宾表单链接",
      "form_busy": "表单正在另一个窗口中创建。请等一分钟，然后使用“检查安装”。",
      "form_exists": "嘉宾表单已经存在。发给嘉宾的链接：{{url}}",
      "form_created": "已创建嘉宾表单（{{variante}}）。发给嘉宾的链接：{{url}} 链接也保存在“配置”标签页中。",
      "form_fail": "无法创建表单：{{motivo}}",
      "variants": {"essencial": "基础版", "completo": "完整版"},
      "item": "配置节目",
      "ask_code_title": "节目代码",
      "ask_code": "请输入 Claude 在聊天中显示的 15 位字母和数字代码（可带或不带短横线）：",
      "done": "节目“{{nome}}”已配置。详细信息在 {{aba}} 标签页中。",
      "tab": "设置",
      "note": "此标签页仅显示设置。如需修改，请在聊天中告诉 Claude，然后再次使用 PodFácil > 配置节目。",
      "labels": {
        "name": "节目",
        "tagline": "介绍语",
        "locale": "语言",
        "editorial": "编辑方向",
        "modes": "录制方式",
        "studio": "录音室",
        "address": "地址",
        "colors": "颜色",
        "logo": "标志",
        "controller": "数据控制者",
        "retention": "回答保存期"
      },
      "retention_days": "发布后 {{dias}} 天",
      "imported": "已导入节目资料“{{nome}}”。",
      "logo_item": "上传标志",
      "import_failed": "节目资料已收到，但无法保存（{{motivo}}）。请让 Claude 重新保存，然后使用 PodFácil > 配置节目。",
      "logo": {
        "title": "邀请函标志",
        "lead": "选择节目标志（PNG 或 JPG，最大 1 MB）。它会嵌入邀请函，并保存在你的 Google 云端硬盘中。",
        "button": "上传",
        "working": "正在上传…",
        "ok": "标志已保存。之后的邀请函都会带上它。",
        "too_big": "文件超过 1 MB。请缩小图片后重试。",
        "bad_type": "请使用 PNG 或 JPG 文件。",
        "need_show": "请先配置节目（PodFácil > 配置节目）。",
        "failed": "上传标志时出错。请重试。"
      }
    }
  },
  "guest_confirm": {
    "subject": "{{show}}：能否确认一下您参与节目的几项信息？",
    "greeting": "{{nome}}，您好！",
    "intro": "感谢您填写 {{show}} 的表单。录制前，我们想确认以下几点：",
    "intro_none": "感谢您填写 {{show}} 的表单。录制前，我们想确认以下信息。",
    "items": {
      "contacts.whatsapp": "我们无法识别您填写的 WhatsApp 号码{{end}}。正确的号码是多少（含国家代码）？",
      "accessibility": "您填写了无障碍方面的需求，但没有勾选允许我们保存此类信息的授权，因此未予记录。如果希望我们提前准备，请回复此邮件，我们再商量如何处理。",
      "scheduled_at": "我们无法识别录制的日期和时间。您什么时候方便？",
      "check.time_odd": "您填写的时间是 {{hora}}。是否正确？",
      "check.past": "您填写的日期（{{data}}）已经过去。正确的日期是哪天？",
      "check.whatsapp_mismatch": "您填写的 WhatsApp 号码尾号为 {{agora}}，但我们记录的号码尾号为 {{antes}}。应该使用哪个？"
    },
    "end": "（尾号 {{digits}}）",
    "summary": "我们记录的信息",
    "labels": {
      "recording": "录制",
      "whatsapp": "WhatsApp"
    },
    "whatsapp_end": "尾号 {{digits}}",
    "closing": "直接回复此邮件告诉我们更正内容即可。如果一切无误，请回复“没问题”。",
    "signature": "{{show}} 团队"
  }
}

```
