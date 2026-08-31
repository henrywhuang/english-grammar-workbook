(() => {
  const data = window.GRAMMAR_DATA;
  const letters = ["A", "B", "C", "D"];
  const state = { view: "outline", topic: 0, answers: {}, graded: false, query: "" };

  const $ = (selector) => document.querySelector(selector);
  const topicList = $("#topicList");
  const topicCount = $("#topicCount");
  const panel = $("#topicPanel");
  const scrim = $("#scrim");

  const escapeHTML = (value) => String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
  const topicNumber = (number) => String(number).padStart(3, "0");
  const currentTopic = () => data.topics[state.topic];

  function setHash() {
    const suffix = state.view === "outline" ? "" : `/${topicNumber(state.topic + 1)}`;
    history.replaceState(null, "", `#${state.view}${suffix}`);
  }

  function readHash() {
    const match = location.hash.match(/^#(outline|practice|answers)(?:\/(\d{1,3}))?/);
    if (!match) return;
    state.view = match[1];
    if (match[2]) state.topic = Math.min(data.topics.length - 1, Math.max(0, Number(match[2]) - 1));
  }

  function closePanel() {
    panel.classList.remove("open");
    scrim.classList.remove("show");
    $(".menu-button").setAttribute("aria-expanded", "false");
  }

  function renderTopicList() {
    const query = state.query.trim().toLowerCase();
    const topics = data.topics.filter(topic => {
      const haystack = `${topicNumber(topic.number)} ${topic.title} ${topic.part} ${topic.section}`.toLowerCase();
      return !query || haystack.includes(query);
    });
    topicCount.textContent = `${topics.length} / ${data.topicCount} 个知识点`;
    let previousPart = "";
    let previousSection = "";
    let previousSubsection = "";
    topicList.innerHTML = topics.length ? topics.map(topic => {
      let headings = "";
      if (topic.part !== previousPart) {
        headings += `<div class="sidebar-part">${escapeHTML(topic.part)}</div>`;
        previousPart = topic.part;
        previousSection = "";
        previousSubsection = "";
      }
      if (topic.section !== previousSection) {
        headings += `<div class="sidebar-section">${escapeHTML(topic.section)}</div>`;
        previousSection = topic.section;
        previousSubsection = "";
      }
      if (topic.subsection && topic.subsection !== previousSubsection) {
        headings += `<div class="sidebar-subsection">${escapeHTML(topic.subsection)}</div>`;
        previousSubsection = topic.subsection;
      }
      return `${headings}<button class="topic-item ${topic.number === state.topic + 1 ? "active" : ""}" data-topic="${topic.number - 1}">
          <span class="number">${topicNumber(topic.number)}</span>
          <span class="label">${escapeHTML(topic.title)}</span>
        </button>`;
    }).join("") : `<div class="empty">没有找到匹配的知识点</div>`;
  }

  function buildHierarchy(topics) {
    const parts = new Map();
    topics.forEach(topic => {
      if (!parts.has(topic.part)) parts.set(topic.part, new Map());
      const sections = parts.get(topic.part);
      if (!sections.has(topic.section)) sections.set(topic.section, new Map());
      const subsections = sections.get(topic.section);
      const key = topic.subsection || "";
      if (!subsections.has(key)) subsections.set(key, []);
      subsections.get(key).push(topic);
    });
    return parts;
  }

  function renderOutline() {
    const hierarchy = buildHierarchy(data.topics);
    $("#outlineView").innerHTML = `
      <div class="hero">
        <div class="eyebrow">Structured learning · 随时练习</div>
        <h1>把英语语法，<br>变成一张清晰的地图。</h1>
        <p class="lead">从词法到句法，循序完成 286 个知识点与 2860 道单选练习。选择任一知识点，即可开始答题或查看答案。</p>
        <div class="stats">
          <div class="stat"><strong>${data.topicCount}</strong><span>语法知识点</span></div>
          <div class="stat"><strong>${data.questionCount.toLocaleString()}</strong><span>互动练习题</span></div>
          <div class="stat"><strong>10</strong><span>每个知识点</span></div>
        </div>
      </div>
      <div class="resource-grid">
        <a class="resource-card" href="assets/outline.pdf" target="_blank"><span class="file-type">PDF · OUTLINE</span><strong>语法知识大纲</strong><small>查看或下载完整结构化目录</small></a>
        <a class="resource-card" href="assets/worksheet.pdf" target="_blank"><span class="file-type">PDF · WORKSHEET</span><strong>完整题目册</strong><small>适合打印与线下练习</small></a>
        <a class="resource-card" href="assets/answers.pdf" target="_blank"><span class="file-type">PDF · ANSWERS</span><strong>完整答案册</strong><small>按知识点快速核对答案</small></a>
      </div>
      ${[...hierarchy.entries()].map(([part, sections]) => `
        <div class="outline-group">
          <div class="level-label">LEVEL 1 · 部分</div>
          <h2 class="part-heading">${escapeHTML(part)}</h2>
          ${[...sections.entries()].map(([section, subsections]) => `
            <section class="chapter-group">
              <div class="level-label">LEVEL 2 · 章节</div>
              <h3>${escapeHTML(section)}</h3>
              ${[...subsections.entries()].map(([subsection, topics]) => `
                <div class="subsection-group">
                  ${subsection ? `<div class="level-label">LEVEL 3 · 小节</div><h4>${escapeHTML(subsection)}</h4>` : ""}
                  <div class="level-label topic-level">LEVEL ${subsection ? "4" : "3"} · 知识点</div>
                  <div class="outline-grid">${topics.map(topic => `
                    <button class="outline-link" data-open-topic="${topic.number - 1}">
                      <b>${topicNumber(topic.number)}</b><span>${escapeHTML(topic.title)}</span>
                    </button>`).join("")}</div>
                </div>`).join("")}
            </section>`).join("")}
        </div>`).join("")}`;
  }

  function heading(topic, label) {
    const path = [topic.part, topic.section, topic.subsection].filter(Boolean).join(" › ");
    return `<div class="topic-heading">
      <div class="eyebrow">${label} · ${topicNumber(topic.number)}</div>
      <h1>${escapeHTML(topic.title)}</h1>
      <div class="breadcrumb">${escapeHTML(path)}</div>
      <div class="topic-actions">
        <button class="button" data-jump="outline">返回大纲</button>
        <button class="button" data-jump="practice">开始答题</button>
        <button class="button" data-jump="answers">查看答案</button>
      </div>
    </div>`;
  }

  function renderPractice() {
    const topic = currentTopic();
    $("#practiceView").innerHTML = `${heading(topic, "Practice")}
      <form id="quizForm">
        ${topic.questions.map((question, qIndex) => `
          <article class="question-card" data-question="${qIndex}">
            <div><span class="question-number">${qIndex + 1}</span><span class="stem">${escapeHTML(question.stem)}</span></div>
            <div class="options">${question.options.map((option, oIndex) => `
              <label class="option">
                <input type="radio" name="q${qIndex}" value="${letters[oIndex]}" ${state.answers[qIndex] === letters[oIndex] ? "checked" : ""}>
                <span><b>${letters[oIndex]}.</b> ${escapeHTML(option)}</span>
              </label>`).join("")}</div>
          </article>`).join("")}
      </form>
      <div class="result-bar">
        <div class="result-copy"><strong id="resultTitle">完成后提交答案</strong><small id="resultDetail">已答 0 / 10 题</small></div>
        <div><button class="button" id="resetQuiz" type="button">重置</button> <button class="button primary" id="gradeQuiz" type="button">提交答案</button></div>
      </div>
      ${pager()}`;
    updateProgress();
  }

  function renderAnswers() {
    const topic = currentTopic();
    $("#answersView").innerHTML = `${heading(topic, "Answer key")}
      <div class="answers-list">${topic.questions.map((question, index) => {
        const answerIndex = letters.indexOf(question.answer);
        return `<div class="answer-row"><div class="answer-badge">${index + 1}.${question.answer}</div><div><p>${escapeHTML(question.options[answerIndex])}</p><small>${escapeHTML(question.stem)}</small></div></div>`;
      }).join("")}</div>${pager()}`;
  }

  function pager() {
    return `<div class="pager">
      <button class="button" data-page="prev" ${state.topic === 0 ? "disabled" : ""}>← 上一知识点</button>
      <button class="button" data-page="next" ${state.topic === data.topics.length - 1 ? "disabled" : ""}>下一知识点 →</button>
    </div>`;
  }

  function updateProgress() {
    const detail = $("#resultDetail");
    if (detail) detail.textContent = `已答 ${Object.keys(state.answers).length} / ${currentTopic().questions.length} 题`;
  }

  function gradeQuiz() {
    state.graded = true;
    let correct = 0;
    currentTopic().questions.forEach((question, index) => {
      const card = document.querySelector(`[data-question="${index}"]`);
      const options = card.querySelectorAll(".option");
      card.classList.remove("correct", "wrong");
      options.forEach((option, optionIndex) => {
        option.classList.remove("answer", "chosen-wrong");
        if (letters[optionIndex] === question.answer) option.classList.add("answer");
        if (letters[optionIndex] === state.answers[index] && state.answers[index] !== question.answer) option.classList.add("chosen-wrong");
      });
      if (state.answers[index] === question.answer) { correct += 1; card.classList.add("correct"); }
      else card.classList.add("wrong");
    });
    $("#resultTitle").textContent = `本次得分：${correct} / ${currentTopic().questions.length}`;
    $("#resultDetail").textContent = correct === 10 ? "全部答对，很棒！" : "绿色为正确答案，可继续修改后重新提交";
  }

  function resetQuiz() {
    state.answers = {};
    state.graded = false;
    renderPractice();
    showToast("本页作答记录已重置");
  }

  function selectTopic(index, view = state.view === "outline" ? "practice" : state.view) {
    state.topic = Number(index);
    state.view = view;
    state.answers = {};
    state.graded = false;
    render();
    closePanel();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function setView(view) {
    state.view = view;
    render();
    closePanel();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function render() {
    document.querySelectorAll(".view").forEach(view => view.classList.remove("active"));
    document.querySelectorAll(".main-nav button").forEach(button => button.classList.toggle("active", button.dataset.view === state.view));
    $(`#${state.view}View`).classList.add("active");
    renderTopicList();
    if (state.view === "outline") renderOutline();
    if (state.view === "practice") renderPractice();
    if (state.view === "answers") renderAnswers();
    setHash();
  }

  function showToast(message) {
    const toast = $("#toast");
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove("show"), 1800);
  }

  document.addEventListener("click", event => {
    const nav = event.target.closest("[data-view]");
    if (nav) setView(nav.dataset.view);
    const topic = event.target.closest("[data-topic]");
    if (topic) selectTopic(topic.dataset.topic);
    const opener = event.target.closest("[data-open-topic]");
    if (opener) selectTopic(opener.dataset.openTopic, "practice");
    const jump = event.target.closest("[data-jump]");
    if (jump) setView(jump.dataset.jump);
    const page = event.target.closest("[data-page]");
    if (page && !page.disabled) selectTopic(state.topic + (page.dataset.page === "next" ? 1 : -1));
    if (event.target.id === "gradeQuiz") gradeQuiz();
    if (event.target.id === "resetQuiz") resetQuiz();
  });

  document.addEventListener("change", event => {
    if (!event.target.matches('#quizForm input[type="radio"]')) return;
    state.answers[Number(event.target.name.slice(1))] = event.target.value;
    updateProgress();
  });

  $("#topicSearch").addEventListener("input", event => { state.query = event.target.value; renderTopicList(); });
  $(".menu-button").addEventListener("click", () => {
    const open = panel.classList.toggle("open");
    scrim.classList.toggle("show", open);
    $(".menu-button").setAttribute("aria-expanded", String(open));
  });
  scrim.addEventListener("click", closePanel);
  window.addEventListener("hashchange", () => { readHash(); render(); });

  readHash();
  render();
})();
