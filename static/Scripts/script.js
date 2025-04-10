const gradePoints = { "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "RA": 0, "U": 0, "AB": 0 };
    let grades = {};

    // 🔄 Refresh index.html if redirected from add_subject.html
    if (localStorage.getItem("refreshIndex") === "true") {
        localStorage.removeItem("refreshIndex");
        location.reload(); // Force reload to reflect newly added subjects
    }

    function saveGrade(selectElem) {
        const code = selectElem.name;
        const grade = selectElem.value;
        const credits = parseFloat(selectElem.getAttribute('data-credits'));
        const semester = selectElem.getAttribute('data-semester');

        if (grade !== '') {
            grades[code] = { grade, credits, semester };
        } else {
            delete grades[code];
        }

        localStorage.setItem("saved_grades", JSON.stringify(grades));
    }

    function calculateSemesterGPA(semester) {
        let totalCredits = 0, totalPoints = 0;

        for (const code in grades) {
            const entry = grades[code];
            if (entry.semester === semester) {
                totalCredits += entry.credits;
                totalPoints += gradePoints[entry.grade] * entry.credits;
            }
        }

        const gpa = totalCredits > 0 ? (totalPoints / totalCredits).toFixed(2) : '0.00';
        document.getElementById('gpa_' + semester.replace(/ /g, '_')).innerText = `📘 GPA for ${semester}: ${gpa}`;
    }

    function calculateCGPA() {
        let totalCredits = 0, totalPoints = 0;

        for (const code in grades) {
            const entry = grades[code];
            totalCredits += entry.credits;
            totalPoints += gradePoints[entry.grade] * entry.credits;
        }

        const cgpa = totalCredits > 0 ? (totalPoints / totalCredits).toFixed(2) : '0.00';
        document.getElementById("cgpa_result").innerText = `🎓 CGPA: ${cgpa}`;
    }

    function removeSubject(semester, code, button) {
        if (!confirm(`Are you sure you want to remove ${code} from ${semester}?`)) return;

        let dynamicSubjects = JSON.parse(localStorage.getItem("dynamic_subjects") || "{}");
        if (dynamicSubjects[semester]) {
            dynamicSubjects[semester] = dynamicSubjects[semester].filter(sub => sub.code !== code);
            localStorage.setItem("dynamic_subjects", JSON.stringify(dynamicSubjects));
        }

        delete grades[code];
        localStorage.setItem("saved_grades", JSON.stringify(grades));

        const row = button.closest("tr");
        if (row) row.remove();
    }

    window.onload = function () {
        const saved = localStorage.getItem("saved_grades");
        if (saved) {
            grades = JSON.parse(saved);
            for (const code in grades) {
                const grade = grades[code].grade;
                const select = document.querySelector(`select[name="${code}"]`);
                if (select) select.value = grade;
            }
        }

        const extraSubjects = JSON.parse(localStorage.getItem("dynamic_subjects") || "{}");
        for (const semester in extraSubjects) {
            const subjectList = extraSubjects[semester];
            const table = document.querySelector(`#table_${semester.replace(/ /g, '_')} tbody`);
            if (table) {
                subjectList.forEach(sub => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td>${sub.code}</td>
                        <td>${sub.name}</td>
                        <td>${sub.credits}</td>
                        <td>
                            <select name="${sub.code}" data-semester="${semester}" data-credits="${sub.credits}" onchange="saveGrade(this)">
                                <option value="">-- Select Grade --</option>
                                <option value="O">O</option>
                                <option value="A+">A+</option>
                                <option value="A">A</option>
                                <option value="B+">B+</option>
                                <option value="B">B</option>
                                <option value="RA">RA</option>
                                <option value="U">U</option>
                                <option value="AB">AB</option>
                            </select>
                            <br>
                            <button class="remove-btn" onclick="removeSubject('${semester}', '${sub.code}', this)">Remove</button>
                        </td>
                    `;
                    table.appendChild(tr);
                });
            }
        }
    };