// Lightweight Voice Assistant using Web Speech API (TTS + STT)
// Non-intrusive: adds a small floating button overlay without changing existing layout

(function () {
  if (typeof window === 'undefined') return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const synth = window.speechSynthesis;

  function speak(text) {
    try {
      if (!synth) return;
      const utter = new SpeechSynthesisUtterance(text);
      utter.rate = 1;
      utter.pitch = 1;
      utter.volume = 1;
      synth.cancel();
      synth.speak(utter);
    } catch (_) {}
  }

  function createUI() {
    const btn = document.createElement('button');
    btn.setAttribute('type', 'button');
    btn.setAttribute('aria-label', 'Voice assistant');
    btn.style.position = 'fixed';
    btn.style.right = '16px';
    btn.style.bottom = '16px';
    btn.style.zIndex = '2147483647';
    btn.style.width = '48px';
    btn.style.height = '48px';
    btn.style.borderRadius = '50%';
    btn.style.border = 'none';
    btn.style.cursor = 'pointer';
    btn.style.boxShadow = '0 6px 16px rgba(0,0,0,0.25)';
    btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    btn.style.color = '#fff';
    btn.style.fontSize = '20px';
    btn.style.display = 'flex';
    btn.style.alignItems = 'center';
    btn.style.justifyContent = 'center';
    btn.style.userSelect = 'none';
    btn.textContent = '🎙️';

    const pulse = document.createElement('div');
    pulse.style.position = 'absolute';
    pulse.style.inset = '-6px';
    pulse.style.borderRadius = '50%';
    pulse.style.border = '2px solid rgba(118,75,162,0.35)';
    pulse.style.animation = 'voice-pulse 1.8s ease-out infinite';
    btn.appendChild(pulse);

    const style = document.createElement('style');
    style.textContent = '@keyframes voice-pulse {0%{transform:scale(0.9);opacity:0.7}70%{transform:scale(1.2);opacity:0}100%{transform:scale(1.2);opacity:0}}';
    document.head.appendChild(style);

    document.body.appendChild(btn);

    // ARIA live region for announcements (polite, non-intrusive)
    const live = document.createElement('div');
    live.setAttribute('aria-live', 'polite');
    live.setAttribute('aria-atomic', 'true');
    live.style.position = 'fixed';
    live.style.left = '-9999px';
    live.style.top = 'auto';
    document.body.appendChild(live);
    btn.__liveRegion = live;
    return btn;
  }

  function initRecognition(onResult, onStart, onEnd) {
    if (!SpeechRecognition) return null;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (e) => {
      const transcript = e.results && e.results[0] && e.results[0][0] ? e.results[0][0].transcript : '';
      onResult && onResult(transcript || '');
    };
    recognition.onstart = () => onStart && onStart();
    recognition.onend = () => onEnd && onEnd();
    recognition.onerror = () => onEnd && onEnd();
    return recognition;
  }

  function normalizeUrlSpoken(text) {
    let u = (text || '').trim();
    u = u.replace(/\s+/g, '');
    u = u.replace(/ dot /g, '.');
    u = u.replace(/ slash /g, '/');
    u = u.replace(/ space /g, '');
    if (!/^https?:\/\//i.test(u)) u = 'https://' + u;
    return u;
  }

  function announce(btn, text) {
    try { if (btn && btn.__liveRegion) btn.__liveRegion.textContent = text; } catch (_) {}
  }

  function handleCommand(commandRaw) {
    const command = (commandRaw || '').toLowerCase().trim();
    if (!command) return;

    // Basic intents
    if (/^(help|what can you do)/.test(command)) {
      speak('You can say: enter url, set url to, submit, scan website, go to report, read scores, read findings, download report, home, back, or stop.');
      return;
    }

    if (/(scan|start).*audit|scan website|start scan/.test(command)) {
      speak('Starting the website scan.');
      try { window.location.href = '/scan'; } catch (_) {}
      return;
    }

    if (/go to report|open report|show report/.test(command)) {
      speak('Opening the report.');
      try { window.location.href = '/report'; } catch (_) {}
      return;
    }

    if (/enter url|go to url|open url page/.test(command)) {
      speak('Opening the URL entry page.');
      try { window.location.href = '/enter-url'; } catch (_) {}
      return;
    }

    // Fill URL field: "set url to ..." or "url is ..." or "scan ..."
    if (/^(set\s+url\s+to\s+|url\s+is\s+|scan\s+)/.test(command)) {
      try {
        const urlText = command.replace(/^(set\s+url\s+to\s+|url\s+is\s+|scan\s+)/, '').trim();
        const normalized = normalizeUrlSpoken(urlText);
        const input = document.querySelector('#website_url');
        if (input) {
          input.value = normalized;
          speak('URL updated. Say submit to start the audit.');
        } else {
          speak('URL input not found on this page.');
        }
      } catch (_) { speak('I could not update the URL.'); }
      return;
    }

    // Submit the form on enter url page
    if (/^(submit|start|begin)($|\s+audit)/.test(command)) {
      try {
        const form = document.querySelector('form[method="POST"]');
        if (form) {
          speak('Submitting the form to start the audit.');
          form.submit();
        } else {
          // fallback to scan page
          speak('Form not found, redirecting to scan.');
          window.location.href = '/scan';
        }
      } catch (_) { speak('I could not submit the form.'); }
      return;
    }

    if (/read score|read scores|read results|tell me the scores/.test(command)) {
      try {
        const sections = [];
        const getScoreFromText = (label) => {
          const el = Array.from(document.querySelectorAll('*'))
            .find(n => n.textContent && n.textContent.trim().toLowerCase() === label);
          if (!el) return null;
          const container = el.closest('.score-card');
          const scoreEl = container ? container.querySelector('.chart-score') : null;
          return scoreEl ? scoreEl.textContent.trim() : null;
        };
        const security = getScoreFromText('🛡️ security') || '';
        const performance = getScoreFromText('⚡ performance') || '';
        const seo = getScoreFromText('🎯 seo') || '';
        const accessibility = getScoreFromText('♿ accessibility') || '';
        const parts = [];
        if (security) parts.push(`Security ${security}`);
        if (performance) parts.push(`Performance ${performance}`);
        if (seo) parts.push(`S E O ${seo}`);
        if (accessibility) parts.push(`Accessibility ${accessibility}`);
        const text = parts.length ? parts.join(', ') : 'Scores are not visible on this page.';
        speak(text);
      } catch (_) {
        speak('Sorry, I cannot read scores on this page.');
      }
      return;
    }

    // Read findings (optionally per category)
    if (/read findings|read (security|performance|seo|accessibility) findings/.test(command)) {
      try {
        const match = command.match(/read (security|performance|seo|accessibility) findings/);
        const category = match ? match[1] : null;
        let containers = Array.from(document.querySelectorAll('.findings-section'));
        if (category) {
          const titlePrefix = {
            'security': '🛡️ Security Analysis',
            'performance': '⚡ Performance Analysis',
            'seo': '🎯 SEO Analysis',
            'accessibility': '♿ Accessibility Analysis'
          }[category];
          containers = containers.filter(c =>
            c.querySelector('h2') && c.querySelector('h2').textContent.trim().toLowerCase() === titlePrefix.toLowerCase()
          );
        }
        const items = containers.flatMap(c => Array.from(c.querySelectorAll('.finding-item')));
        if (!items.length) { speak('No findings are visible to read.'); return; }
        // Keep an index on window to allow next/previous
        const key = '__vaFindingIndex';
        if (typeof window[key] !== 'number') window[key] = 0;
        const clamp = (i) => Math.max(0, Math.min(items.length - 1, i));
        const i = clamp(window[key]);
        const item = items[i];
        const title = item.querySelector('h4')?.textContent?.trim() || `Finding ${i+1}`;
        const desc = item.querySelector('p')?.textContent?.trim() || '';
        const steps = Array.from(item.querySelectorAll('.fix-steps li')).slice(0, 3).map((li, j) => `Step ${j+1}. ${li.textContent.trim()}`);
        const msg = [title, desc].concat(steps).join('. ');
        speak(msg);
        announce(document.querySelector('button[aria-label="Voice assistant"]'), msg);
      } catch (_) { speak('I could not read the findings.'); }
      return;
    }

    // Next/Previous finding
    if (/next finding|read next/.test(command)) {
      try { window.__vaFindingIndex = (typeof window.__vaFindingIndex==='number'? window.__vaFindingIndex+1:1); speak('Next finding. Say read findings to hear it.'); } catch(_){}
      return;
    }
    if (/previous finding|read previous/.test(command)) {
      try { window.__vaFindingIndex = (typeof window.__vaFindingIndex==='number'? Math.max(0, window.__vaFindingIndex-1):0); speak('Previous finding. Say read findings to hear it.'); } catch(_){}
      return;
    }

    // Download report
    if (/download report|save report/.test(command)) {
      speak('Downloading the PDF report.');
      try { window.location.href = '/download-report'; } catch (_) {}
      return;
    }

    // Navigation helpers
    if (/^home$|go home|go to home|open home/.test(command)) {
      speak('Going to the home page.');
      try { window.location.href = '/'; } catch (_) {}
      return;
    }

    if (/go back|back/.test(command)) {
      speak('Going back.');
      try { history.back(); } catch (_) {}
      return;
    }

    if (/reload|refresh/.test(command)) {
      speak('Reloading the page.');
      try { location.reload(); } catch (_) {}
      return;
    }

    if (/stop|be quiet|mute/.test(command)) {
      try { synth && synth.cancel(); } catch (_) {}
      speak('');
      return;
    }

    // Fallback: read page title
    try {
      const title = document.title || 'this page';
      speak(`You said: ${command}. You are on ${title}. Say help to learn commands.`);
    } catch (_) {}
  }

  function main() {
    const btn = createUI();
    let listening = false;
    let continuous = false;
    const recognition = initRecognition(
      (text) => handleCommand(text),
      () => { listening = true; btn.style.filter = 'brightness(1.1)'; btn.textContent = '🗣️'; },
      () => { listening = false; btn.style.filter = 'none'; btn.textContent = '🎙️'; if (continuous) { try { recognition.start(); } catch (_) {} } }
    );
    if (recognition) recognition.continuous = false;

    btn.addEventListener('click', function () {
      if (!recognition) {
        speak('Speech recognition is not supported in this browser.');
        return;
      }
      try {
        if (listening) {
          recognition.stop();
        } else {
          recognition.start();
          speak('Listening. You can say: enter url, set url to, submit, scan website, read scores, or read findings.');
        }
      } catch (_) {}
    });

    // Double click toggles continuous listening
    btn.addEventListener('dblclick', function () {
      if (!recognition) return;
      continuous = !continuous;
      recognition.continuous = continuous;
      speak(continuous ? 'Continuous listening enabled.' : 'Continuous listening disabled.');
    });

    // Optional: greet on first load (polite, short)
    setTimeout(function () {
      speak('Voice assistant ready. Click the microphone to give a command.');
    }, 800);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', main);
  } else {
    main();
  }
})();


