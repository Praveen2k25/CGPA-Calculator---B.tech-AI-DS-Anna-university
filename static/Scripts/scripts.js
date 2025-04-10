function addSubject(semester, code, name, credits) {
    const subject = { code, name, credits: parseFloat(credits) };
    let dynamicSubjects = JSON.parse(localStorage.getItem('dynamic_subjects')) || {};

    if (!dynamicSubjects[semester]) {
        dynamicSubjects[semester] = [];
    }

    const exists = dynamicSubjects[semester].some(sub => sub.code === code);
    const msgElem = document.getElementById("statusMsg");

    if (!exists) {
        dynamicSubjects[semester].push(subject);
        localStorage.setItem("dynamic_subjects", JSON.stringify(dynamicSubjects));

        // ✅ Set refresh flag
        localStorage.setItem("refreshIndex", "true");

        // ✅ Redirect to index.html
        window.location.href = "/";  // or "/index.html" if running locally without Flask

    } else {
        msgElem.innerText = `⚠️ ${code} already exists in ${semester}`;
        msgElem.style.color = 'orange';
        msgElem.classList.add('show');

        // Auto-hide after 3 seconds
        setTimeout(() => {
            msgElem.classList.remove('show');
        }, 3000);
    }
}
