const title = document.getElementById("title");
title.textContent = "My Expenses";

const form = document.getElementById("expense_form");
const expenses_list = document.getElementById("list_expenses")

let editingExpenseId = null;

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
        amount: Number(document.getElementById("amount").value),
        category: document.getElementById("category").value,
        description: document.getElementById("description").value,
    }
    try {
        if (editingExpenseId === null) {
            await add_expense(data);
        } else {
            await update_expense(editingExpenseId, data);
            editingExpenseId = null;
        }
        
        await get_expenses();
        form.reset();
        document.getElementById("submit_btn").value = "Add Expense";

    } catch (error) {
        console.error(error);
        alert(error.message)
    }

})

async function get_expenses() {
    const response = await fetch("http://127.0.0.1:8000/expenses/");
    const expenses = await response.json();
    
    expenses_list.innerHTML = "";
    expenses.forEach(expense => {
        const new_element = document.createElement("li");
        const update_btn = document.createElement("button");

        update_btn.textContent = "Update";
        update_btn.addEventListener("click", () => {
            editingExpenseId = expense.id;
            document.getElementById("amount").value = expense.amount;
            document.getElementById("category").value = expense.category;
            document.getElementById("description").value = expense.description;
            document.getElementById("submit_btn").value = "Update";
        });

        const delete_btn = document.createElement("button");
        delete_btn.textContent = "Delete";
        delete_btn.addEventListener("click", async () => {
            try {
                await delete_expense(expense.id);
                await get_expenses();
            } catch (error) {
                console.error(error);
                alert(error.message);
            }
        });

        new_element.textContent = `category: ${expense.category}, amount: ${expense.amount}, description: ${expense.description}`;
        expenses_list.appendChild(new_element);
        expenses_list.appendChild(update_btn);
        expenses_list.appendChild(delete_btn);
    });
    
}

async function delete_expense(id) {
    const response = await fetch(`http://127.0.0.1:8000/expenses/${id}`, {
        method: "DELETE"
    });
    if (!response.ok) {
        throw new Error("Error when deleting expense");
    }
}

async function update_expense(id, data) {
    const response = await fetch(`http://127.0.0.1:8000/expenses/${id}`, {
        method: "PUT",
        headers: {
            "Content-type" : "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail?.[0]?.msg || "Error when updating");
    }

    return await response.json()
    
}

async function add_expense(data) {
    const response = await fetch("http://127.0.0.1:8000/expenses/", {
        method: "POST",
        headers: {
            "Content-type" : "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail?.[0]?.msg || "Error when adding");
    }

    return await response.json();
    
}

get_expenses();