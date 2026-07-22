let table;

const message = document.getElementById("message");
const searchInput = document.getElementById("search");

const requiredFields = [
    "date",
    "time",
    "patient",
    "cpf",
    "doctor",
    "specialty",
    "insurance",
    "status"
];

function showError(errorMessage) {
    message.textContent = errorMessage;
    message.classList.add("error-message");
}

function validateAppointments(data) {
    if (!Array.isArray(data)) {
        throw new Error("A API retornou uma resposta inválida.");
    }

    for (const appointment of data) {
        const missingFields = requiredFields.filter(function (field) {
            return (
                !(field in appointment) ||
                appointment[field] === null ||
                appointment[field] === ""
            );
        });

        if (missingFields.length > 0) {
            console.error(
                "Campos obrigatórios ausentes:",
                missingFields,
                appointment
            );

            throw new Error(
                "Um ou mais agendamentos possuem campos obrigatórios ausentes."
            );
        }
    }
}

fetch("/api/appointments")
    .then(async function (response) {
        if (!response.ok) {
            if (response.status === 503) {
                throw new Error(
                    "O serviço está temporariamente indisponível. Tente novamente."
                );
            }

            throw new Error(
                "Não foi possível carregar os agendamentos."
            );
        }

        const responseText = await response.text();

        if (!responseText.trim()) {
            throw new Error(
                "A API retornou uma resposta vazia."
            );
        }

        try {
            return JSON.parse(responseText);
        } catch (error) {
            throw new Error(
                "A API retornou uma resposta inválida."
            );
        }
    })

    .then(function (data) {
        validateAppointments(data);

        message.classList.remove("error-message");

        if (data.length === 0) {
            message.textContent =
                "Nenhum agendamento encontrado.";
        } else {
            message.textContent =
                `${data.length} agendamento(s) encontrado(s).`;
        }

        table = new Tabulator("#appointments-table", {
            data: data,
            layout: "fitColumns",
            pagination: true,
            paginationSize: 5,
            placeholder: "Nenhum agendamento encontrado.",

            columns: [
                { title: "Data", field: "date" },
                { title: "Horário", field: "time" },
                { title: "Paciente", field: "patient" },
                { title: "CPF", field: "cpf" },
                { title: "Médico", field: "doctor" },
                {
                    title: "Especialidade",
                    field: "specialty"
                },
                { title: "Convênio", field: "insurance" },
                { title: "Status", field: "status" }
            ]
        });
    })

    .catch(function (error) {
        console.error(
            "Erro ao carregar os agendamentos:",
            error
        );

        showError(error.message);
    });

searchInput.addEventListener("keyup", function () {
    const value = this.value.trim();

    if (!table) {
        return;
    }

    if (value === "") {
        table.clearFilter();

        const total = table.getDataCount();

        if (total === 0) {
            message.textContent =
                "Nenhum agendamento encontrado.";
        } else {
            message.textContent =
                `${total} agendamento(s) encontrado(s).`;
        }

        return;
    }

    table.setFilter([
        [
            {
                field: "patient",
                type: "like",
                value: value
            },
            {
                field: "cpf",
                type: "like",
                value: value
            }
        ]
    ]);

    const filteredCount = table.getDataCount("active");

    if (filteredCount === 0) {
        message.textContent =
            "Nenhum agendamento encontrado.";
    } else {
        message.textContent =
            `${filteredCount} agendamento(s) encontrado(s).`;
    }
});