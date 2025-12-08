import { EditorView, basicSetup } from 'https://unpkg.com/@codemirror/basic-setup@0.19.2/dist/index.js';
import { javascript } from 'https://unpkg.com/@codemirror/lang-javascript@0.19.3/dist/index.js';
import { python } from 'https://unpkg.com/@codemirror/lang-python@0.19.3/dist/index.js';

const socket = io();
const output = document.getElementById('output');
const newBtn = document.getElementById('new');
const runBtn = document.getElementById('run');
const langSelect = document.getElementById('lang');

let currentRoom = window.location.pathname.slice(1) || null;

async function initEditor() {
  const startDoc = `// Start coding...`;
  window.editor = new EditorView({
    doc: startDoc,
    extensions: [basicSetup],
    parent: document.getElementById('editor')
  });
  // apply language mode
  setLanguage(langSelect.value);

  let changeTimer = null;
  window.editor.dispatch = ((origDispatch => (tr) => {
    origDispatch.call(window.editor, tr);
    if (changeTimer) clearTimeout(changeTimer);
    changeTimer = setTimeout(() => {
      const code = window.editor.state.doc.toString();
      if (currentRoom) socket.emit('code_change', { room: currentRoom, code, lang: langSelect.value });
    }, 200);
  })(window.editor.dispatch));
}

function setLanguage(lang) {
  if (!window.editor) return;
  const state = window.editor.state;
  let langExt = null;
  if (lang === 'javascript') langExt = javascript();
  if (lang === 'python') langExt = python();
  if (langExt) window.editor.dispatch({ effects: state.updateListener });
  // For simplicity CodeMirror lang integration is minimal in this demo
}

socket.on('connect', () => {
  if (currentRoom) socket.emit('join', currentRoom);
});

socket.on('code_update', (payload) => {
  const code = payload.code || '';
  const cursor = window.editor.state.selection.main.head;
  window.editor.dispatch({ changes: { from: 0, to: window.editor.state.doc.length, insert: code } });
  // restore cursor
  window.editor.dispatch({ selection: { anchor: cursor } });
});

socket.on('lang_update', (payload) => {
  langSelect.value = payload.lang;
  setLanguage(payload.lang);
});

newBtn.addEventListener('click', async () => {
  const res = await fetch('/new');
  const data = await res.json();
  window.location = data.url;
});

langSelect.addEventListener('change', () => {
  const lang = langSelect.value;
  if (currentRoom) socket.emit('lang_change', { room: currentRoom, lang });
  setLanguage(lang);
});

runBtn.addEventListener('click', async () => {
  const code = window.editor.state.doc.toString();
  output.innerText = 'Running...';
  const lang = langSelect.value;
  try {
    if (lang === 'python') {
      // load pyodide if not already
      if (!window.pyodide) {
        output.innerText = 'Loading Pyodide (first run)...';
        await loadPyodide();
      }
      const result = await window.pyodide.runPythonAsync(code);
      output.innerText = String(result);
    } else if (lang === 'javascript') {
      // quickjs via CDN (if available)
      if (window.QuickJS) {
        const qj = await window.QuickJS();
        const result = qj.evalCode(code);
        output.innerText = result.value || '';
        qj.dispose();
      } else {
        // fallback to iframe sandboxed eval
        const iframe = document.createElement('iframe');
        iframe.sandbox = 'allow-scripts';
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        const script = iframe.contentWindow.document.createElement('script');
        script.innerHTML = `try{console.log=parent.postMessage; var r = (function(){${code}})(); parent.postMessage({type:'run-result', result: r}, '*')}catch(e){parent.postMessage({type:'run-error', error: String(e)}, '*')}`;
        window.addEventListener('message', function onmsg(ev){
          if (ev.data && ev.data.type === 'run-result') {
            output.innerText = JSON.stringify(ev.data.result);
            window.removeEventListener('message', onmsg);
            document.body.removeChild(iframe);
          }
          if (ev.data && ev.data.type === 'run-error') {
            output.innerText = 'Error: ' + ev.data.error;
            window.removeEventListener('message', onmsg);
            document.body.removeChild(iframe);
          }
        });
        iframe.contentWindow.document.body.appendChild(script);
      }
    }
  } catch (err) {
    output.innerText = 'Error: ' + String(err);
  }
});

async function loadPyodide() {
  if (window.pyodide) return;
  // load pyodide from CDN
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.2/full/pyodide.js';
  document.head.appendChild(script);
  await new Promise((resolve) => { script.onload = resolve; });
  window.pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.2/full/' });
}

initEditor();
