import './App.css'
import ExpenseItem from "./ExpenseItem";
import ExpenseForm from './ExpenseForm';
import { useEffect, useState } from 'react';



function App() {
  const [expenses, setExpenses] = useState([]);
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  function resetForm() {
    setAmount("");
    setCategory("");
    setDescription("");
    setEditingId(null);
  }

  function startEdit(expense) {
    setEditingId(expense.id);
    setAmount(expense.amount);
    setCategory(expense.category);
    setDescription(expense.description);
  }

  async function addExpense(data) {
    setError("");

    const response = await fetch("http://127.0.0.1:8000/expenses/", {
      method: "POST",
      headers: {
        "Content-Type" : "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Failed to create expense")
    }

    const createdExpense = await response.json();
    
    setExpenses((currentExpenses) => [...currentExpenses, createdExpense]);
    
  }

  async function updateExpense(id, data) {
    const response = await fetch(`http://127.0.0.1:8000/expenses/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type" : "application/json",
      },
      body: JSON.stringify(data),
    });


    if (!response.ok) {
      throw new Error("Failed to update expense");
    }

    const updatedExpense = await response.json();
    
    setExpenses((currentExpenses) => currentExpenses.map((expense) => 
      expense.id === updatedExpense.id
      ? updatedExpense
      : expense
    ));
  }

  async function getExpenses() {
    try {
      setError("");
      const response = await fetch("http://127.0.0.1:8000/expenses/");

      if (!response.ok) {
        throw new Error("Failed to load expenses")
      }

      const data = await response.json();
      setExpenses(data);
      
    } catch (error) {
      setError(error.message);
    }
  }

  useEffect(() => {getExpenses();}, []);

  async function deleteExpense(id) {
    try {
      setError("");
      const response = await fetch(`http://127.0.0.1:8000/expenses/${id}`, {
      method: "DELETE",
    });
    
    if (!response.ok) {
      throw new Error("Failed to delete expense");
    }
    setExpenses((currentExpenses) => currentExpenses.filter((expense) => expense.id !== id));
    } catch (error) {
      setError(error.message);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const data = {
      amount : Number(amount),
      category,
      description,
    }

    try {
      setError("");

      if (editingId === null) {
        await addExpense(data);
      } else {
        await updateExpense(editingId, data);
      }
      resetForm();

    } catch (error) {
      setError(error.message)
    }
    
    
  }


  return (
    <div>
      <h1>Expense Tracker</h1>   
      <ExpenseForm
        amount = {amount} 
        category = {category}
        description = {description}
        onSubmit = {handleSubmit}
        onAmountChange = {(e) => setAmount(e.target.value)}
        onCategoryChange = {(e) => setCategory(e.target.value)}
        onDescriptionChange = {(e) => setDescription(e.target.value)}
        editingId = {editingId} >
      </ExpenseForm>  

      {error && <p>{error}</p>}

      <ul>
        {expenses.map((expense) => (
        <li key={expense.id} >
          <ExpenseItem amount={expense.amount} category={expense.category} description={expense.description}></ExpenseItem>
          <button onClick={() => startEdit(expense)}>Update</button>
          <button onClick={() => deleteExpense(expense.id)}>Delete</button>
        </li>
        ))}
      </ul>
    </div>
  );
}

export default App


