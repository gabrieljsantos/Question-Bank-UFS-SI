"use strict";

const QUESTIONS_FOLDER = "questions";
const INDEX_FILE = `${QUESTIONS_FOLDER}/index.json`;
const METADATA_FILE = "metadata.json";

const app = document.getElementById("app");

marked.setOptions({
    gfm: true,
    breaks: false,
    mangle: false,
    headerIds: false,
});

function encodePath(path) {
    return String(path)
        .split("/")
        .filter(Boolean)
        .map((part) => encodeURIComponent(part))
        .join("/");
}

function questionBaseUrl(folderName) {
    return new URL(
        `./${QUESTIONS_FOLDER}/${encodePath(folderName)}/`,
        window.location.href,
    );
}

function fileUrl(baseUrl, relativePath) {
    return new URL(encodePath(relativePath), baseUrl);
}

async function fetchJson(url) {
    const response = await fetch(url, { cache: "no-store" });

    if (!response.ok) {
        throw new Error(`Não foi possível carregar ${url} (${response.status}).`);
    }

    return response.json();
}

async function fetchText(url) {
    const response = await fetch(url, { cache: "no-store" });

    if (!response.ok) {
        throw new Error(`Não foi possível carregar ${url} (${response.status}).`);
    }

    return response.text();
}

function valueOrFallback(value, fallback) {
    const normalized = String(value ?? "").trim();
    return normalized || fallback;
}

function getClassName(metadata) {
    return valueOrFallback(
        metadata.class_name ??
            metadata.class ??
            metadata.turma ??
            metadata.term,
        "Turma não informada",
    );
}

function getAssessment(metadata) {
    return valueOrFallback(metadata.assessment, "Não informada");
}

function getQuestionLabel(metadata) {
    const tag = valueOrFallback(metadata.tag, "sem_tag");
    const id = valueOrFallback(metadata.id, "sem_id");
    return `${tag} - ID-${id}`;
}

function groupQuestions(items) {
    const grouped = new Map();

    for (const item of items) {
        const metadata = item.metadata;
        const discipline = valueOrFallback(
            metadata.discipline,
            "Disciplina não informada",
        );
        const disciplineCode = valueOrFallback(
            metadata.discipline_code,
            "Código não informado",
        );
        const disciplineKey = `${discipline} - ${disciplineCode}`;

        const professor = valueOrFallback(
            metadata.professor,
            "Professor não informado",
        );
        const className = getClassName(metadata);
        const professorKey = `${professor} - ${className}`;
        const assessmentKey = `Avaliação - ${getAssessment(metadata)}`;

        if (!grouped.has(disciplineKey)) {
            grouped.set(disciplineKey, new Map());
        }

        const professorGroups = grouped.get(disciplineKey);

        if (!professorGroups.has(professorKey)) {
            professorGroups.set(professorKey, new Map());
        }

        const assessmentGroups = professorGroups.get(professorKey);

        if (!assessmentGroups.has(assessmentKey)) {
            assessmentGroups.set(assessmentKey, []);
        }

        assessmentGroups.get(assessmentKey).push(item);
    }

    return grouped;
}

function compareText(a, b) {
    return a.localeCompare(b, "pt-BR", {
        sensitivity: "base",
        numeric: true,
    });
}

function sortMap(map) {
    return [...map.entries()].sort(([a], [b]) => compareText(a, b));
}

async function loadIndexEntries() {
    const index = await fetchJson(`./${INDEX_FILE}`);

    if (!index || !Array.isArray(index.folders)) {
        throw new Error('O arquivo questions/index.json deve conter o campo "folders" como lista.');
    }

    const results = await Promise.allSettled(
        index.folders.map(async (folderName) => {
            const baseUrl = questionBaseUrl(folderName);
            const metadata = await fetchJson(
                fileUrl(baseUrl, METADATA_FILE).href,
            );

            return {
                folderName,
                metadata,
            };
        }),
    );

    const loaded = [];
    const errors = [];

    for (const result of results) {
        if (result.status === "fulfilled") {
            loaded.push(result.value);
        } else {
            errors.push(result.reason);
        }
    }

    if (loaded.length === 0 && errors.length > 0) {
        throw errors[0];
    }

    return { loaded, errors };
}

function createElement(tagName, options = {}) {
    const element = document.createElement(tagName);

    if (options.className) {
        element.className = options.className;
    }

    if (options.text !== undefined) {
        element.textContent = options.text;
    }

    if (options.attributes) {
        for (const [name, value] of Object.entries(options.attributes)) {
            element.setAttribute(name, value);
        }
    }

    return element;
}

async function renderSummary() {
    app.replaceChildren(
        createElement("div", {
            className: "loading",
            text: "Carregando banco de questões...",
        }),
    );

    const { loaded, errors } = await loadIndexEntries();

    if (loaded.length === 0) {
        app.replaceChildren(
            createElement("div", {
                className: "empty-state",
                text: "Nenhuma questão foi encontrada em questions/index.json.",
            }),
        );
        return;
    }

    const fragment = document.createDocumentFragment();
    const grouped = groupQuestions(loaded);

    for (const [discipline, professors] of sortMap(grouped)) {
        const disciplineSection = createElement("section", {
            className: "summary-discipline",
        });

        disciplineSection.appendChild(
            createElement("h1", {
                className: "summary-discipline-title",
                text: discipline,
            }),
        );

        for (const [professor, assessments] of sortMap(professors)) {
            const professorGroup = createElement("section", {
                className: "summary-professor-group",
            });

            professorGroup.appendChild(
                createElement("h2", {
                    className: "summary-professor",
                    text: professor,
                }),
            );

            for (const [assessment, questions] of sortMap(assessments)) {
                const assessmentGroup = createElement("section", {
                    className: "summary-assessment-group",
                });

                assessmentGroup.appendChild(
                    createElement("h3", {
                        className: "summary-assessment",
                        text: assessment,
                    }),
                );

                const questionList = createElement("ul", {
                    className: "summary-question-list",
                });

                questions.sort((a, b) =>
                    compareText(
                        getQuestionLabel(a.metadata),
                        getQuestionLabel(b.metadata),
                    ),
                );

                for (const question of questions) {
                    const item = createElement("li", {
                        className: "summary-question",
                    });
                    const link = createElement("a", {
                        text: getQuestionLabel(question.metadata),
                        attributes: {
                            href: `?question=${encodeURIComponent(
                                question.folderName,
                            )}`,
                        },
                    });

                    item.appendChild(link);
                    questionList.appendChild(item);
                }

                assessmentGroup.appendChild(questionList);
                professorGroup.appendChild(assessmentGroup);
            }

            disciplineSection.appendChild(professorGroup);
        }

        fragment.appendChild(disciplineSection);
    }

    if (errors.length > 0) {
        const warning = createElement("div", { className: "error-box" });
        warning.appendChild(
            createElement("strong", {
                text: "Algumas questões não puderam ser carregadas.",
            }),
        );
        warning.appendChild(
            createElement("div", {
                text: `${errors.length} pasta(s) foram ignoradas por erro de leitura.`,
            }),
        );
        fragment.appendChild(warning);
    }

    app.replaceChildren(fragment);
}

function sanitizeRenderedMarkdown(html) {
    return DOMPurify.sanitize(html, {
        USE_PROFILES: { html: true },
        ADD_ATTR: ["target", "rel"],
    });
}

function renderMarkdown(markdown, baseUrl) {
    const wrapper = createElement("div", { className: "markdown-body" });
    const rendered = marked.parse(markdown || "");
    wrapper.innerHTML = sanitizeRenderedMarkdown(rendered);

    for (const image of wrapper.querySelectorAll("img[src]")) {
        const src = image.getAttribute("src");

        if (src && !isAbsoluteReference(src)) {
            image.src = new URL(src, baseUrl).href;
        }

        image.loading = "lazy";
    }

    for (const link of wrapper.querySelectorAll("a[href]")) {
        const href = link.getAttribute("href");

        if (href && !isAbsoluteReference(href) && !href.startsWith("#")) {
            link.href = new URL(href, baseUrl).href;
        }

        if (/^https?:/i.test(link.href)) {
            link.target = "_blank";
            link.rel = "noopener noreferrer";
        }
    }

    return wrapper;
}

function isAbsoluteReference(value) {
    return /^(?:[a-z][a-z\d+.-]*:|\/\/|\/)/i.test(value);
}

async function copyText(text, button) {
    try {
        await navigator.clipboard.writeText(text);
    } catch {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        textarea.remove();
    }

    const originalText = button.textContent;
    button.textContent = "Copiado";
    button.dataset.copied = "true";

    window.setTimeout(() => {
        button.textContent = originalText;
        delete button.dataset.copied;
    }, 1500);
}

function createContentBlock({ label, rawContent, renderedContent, extraClass }) {
    const block = createElement("section", {
        className: `content-block ${extraClass || ""}`.trim(),
    });
    const header = createElement("header", { className: "block-header" });
    const title = createElement("h2", {
        className: "block-label",
        text: label,
    });
    const copyButton = createElement("button", {
        className: "copy-button",
        text: "Copiar",
        attributes: { type: "button" },
    });
    const content = createElement("div", { className: "block-content" });

    copyButton.addEventListener("click", () =>
        copyText(rawContent, copyButton),
    );

    header.append(title, copyButton);
    content.appendChild(renderedContent);
    block.append(header, content);

    return block;
}

async function renderQuestion(folderName) {
    app.replaceChildren(
        createElement("div", {
            className: "loading",
            text: "Carregando questão...",
        }),
    );

    const baseUrl = questionBaseUrl(folderName);
    const metadata = await fetchJson(fileUrl(baseUrl, METADATA_FILE).href);
    const questionFile = valueOrFallback(
        metadata?.files?.question,
        "question.md",
    );
    const answerFiles = Array.isArray(metadata?.files?.answers)
        ? metadata.files.answers
        : [];

    const questionMarkdown = await fetchText(
        fileUrl(baseUrl, questionFile).href,
    );

    const answerResults = await Promise.allSettled(
        answerFiles.map(async (answerFile) => ({
            answerFile,
            markdown: await fetchText(fileUrl(baseUrl, answerFile).href),
        })),
    );

    const fragment = document.createDocumentFragment();

    const metadataJson = JSON.stringify(metadata, null, 4);
    const metadataMarkdown = `\`\`\`json\n${metadataJson}\n\`\`\``;

    fragment.appendChild(
        createContentBlock({
            label: "Metadados",
            rawContent: metadataJson,
            renderedContent: renderMarkdown(metadataMarkdown, baseUrl),
            extraClass: "metadata-block",
        }),
    );

    fragment.appendChild(
        createContentBlock({
            label: "Questão",
            rawContent: questionMarkdown,
            renderedContent: renderMarkdown(questionMarkdown, baseUrl),
        }),
    );

    let answerNumber = 0;

    for (const result of answerResults) {
        answerNumber += 1;

        if (result.status === "rejected") {
            const errorContent = createElement("div", {
                className: "error-box",
                text: `Não foi possível carregar a resposta ${answerNumber}.`,
            });
            fragment.appendChild(errorContent);
            continue;
        }

        const { answerFile, markdown } = result.value;
        fragment.appendChild(
            createContentBlock({
                label: `Resposta ${answerNumber} — ${answerFile}`,
                rawContent: markdown,
                renderedContent: renderMarkdown(markdown, baseUrl),
            }),
        );
    }

    app.replaceChildren(fragment);
}

function renderFatalError(error) {
    const box = createElement("div", { className: "error-box" });
    box.appendChild(
        createElement("strong", { text: "Não foi possível abrir o banco." }),
    );
    box.appendChild(
        createElement("div", {
            text: error instanceof Error ? error.message : String(error),
        }),
    );
    box.appendChild(
        createElement("p", {
            text: "Abra esta pasta por um servidor HTTP local. Exemplo: python -m http.server 8000",
        }),
    );
    app.replaceChildren(box);
}

async function main() {
    try {
        const params = new URLSearchParams(window.location.search);
        const folderName = params.get("question");

        if (folderName) {
            await renderQuestion(folderName);
        } else {
            await renderSummary();
        }
    } catch (error) {
        console.error(error);
        renderFatalError(error);
    }
}

main();
