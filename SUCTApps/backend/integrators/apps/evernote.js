import dotenv from 'dotenv';
dotenv.config();

import Evernote from 'evernote';
import fs from 'fs/promises';


var callbackUrl = "http://localhost:3000/oauth_callback"; // your endpoint
 
// initialize OAuth
var Evernote = require('evernote');
var client = new Evernote.Client({
  consumerKey: 'my-consumer-key',
  consumerSecret: 'my-consumer-secret',
  sandbox: true, // change to false when you are ready to switch to production
  china: false, // change to true if you wish to connect to YXBJ - most of you won't
});
 
client.getRequestToken(callbackUrl, function(error, oauthToken, oauthTokenSecret) {
  if (error) {
    // do your error handling here
  }
  // store your token here somewhere - for this example we use req.session
  req.session.oauthToken = oauthToken;
  req.session.oauthTokenSecret = oauthTokenSecret;
  res.redirect(client.getAuthorizeUrl(oauthToken)); // send the user to Evernote
});
 
// at callbackUrl - "http://localhost:3000/oauth_callback" in our example. User sent here after Evernote auth
var client = new Evernote.Client({
  consumerKey: 'my-consumer-key',
  consumerSecret: 'my-consumer-secret',
  sandbox: true,
  china: false,
});
client.getAccessToken(req.session.oauthToken,
  req.session.oauthTokenSecret,
  req.query.oauth_verifier,
function(error, oauthToken, oauthTokenSecret, results) {
  if (error) {
    // do your error handling
  } else {
    // oauthAccessToken is the token you need;
    var authenticatedClient = new Evernote.Client({
      token: oauthToken,
      sandbox: true,
      china: false,
    });
    var noteStore = authenticatedClient.getNoteStore();
    noteStore.listNotebooks().then(function(notebooks) {
      console.log(notebooks); // the user's notebooks!
    });
  }
});



var client = new Evernote.Client(token: token);
var userStore = client.getUserStore();
userStore.getUser().then(function(user) {
  // user is the returned User object
});

var Evernote = require('evernote');
var client = new Evernote.Client(token: token);
var noteStore = client.getNoteStore();
var filter = new Evernote.NoteStore.NoteFilter({
  words: ['one', 'two', 'three'],
  ascending: true
});
var spec = new Evernote.NoteStore.NotesMetadataResultSpec({
  includeTitle: true,
  includeContentLength: true,
  includeCreated: true,
  includeUpdated: true,
  includeDeleted: true,
  includeUpdateSequenceNum: true,
  includeNotebookGuid: true,
  includeTagGuids: true,
  includeAttributes: true,
  includeLargestResourceMime: true,
  includeLargestResourceSize: true,
});
 
noteStore.findNotesMetadata(filter, 0, 500, spec).then(function(notesMetadataList) {
  // data.notes is the list of matching notes
});

var linkedNotebook = noteStore.listLinkedNotebooks().then(function(linkedNotebooks) {
  // just pick the first LinkedNotebook for this example
  return client.getSharedNoteStore(linkedNotebooks[0]);
}).then(function(sharedNoteStore) {
  return sharedNoteStore.listNotebooks().then(function(notebooks) {
    return sharedNoteStore.listTagsByNotebook(notebooks[0].guid);
  }).then(function(tags) {
    // tags here is a list of Tag objects
  });
});


var client = new Evernote.Client(token: token);
var noteStore = client.getBusinessNoteStore();
noteStore.listNotebooks(function(notebooks) {
  // notebooks here is the list of notebook objects
});



const token = process.env.EVERNOTE_TOKEN;

if (!token) {
  console.error("Missing EVERNOTE_TOKEN in .env");
  process.exit(1);
}

const client = new Evernote.Client({ token, sandbox: false });
const noteStore = client.getNoteStore();

async function exportAllNotes() {
  try {
    const notebooks = await noteStore.listNotebooks();
    console.log(`Found ${notebooks.length} notebooks`);

    for (const notebook of notebooks) {
      const filter = new Evernote.NoteStore.NoteFilter({ notebookGuid: notebook.guid });
      const spec = new Evernote.NoteStore.NotesMetadataResultSpec({ includeTitle: true });
      const noteList = await noteStore.findNotesMetadata(filter, 0, 10000, spec);

      const notes = [];

      for (const meta of noteList.notes) {
        const note = await noteStore.getNote(meta.guid, true, true, false, false);
        notes.push({
          title: note.title,
          content: note.content,  // ENML format (Evernote's XML)
          tags: note.tagNames || [],
        });
      }

      // Save to JSON
      const filename = `notes-${notebook.name.replace(/\s+/g, '_')}.json`;
      await fs.writeFile(filename, JSON.stringify(notes, null, 2));
      console.log(`Exported ${notes.length} notes from '${notebook.name}' to ${filename}`);
    }

    console.log("✅ Export complete.");

  } catch (err) {
    console.error("❌ Error exporting notes:", err);
  }
}

exportAllNotes();
