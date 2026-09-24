function ExpenseForm ({ amount, category, description, onSubmit, onAmountChange, onCategoryChange, onDescriptionChange, editingId }) {
    return (
        <form onSubmit={onSubmit}>
            <label>
            Amount : <input value={amount} onChange={onAmountChange} />
            </label>
            <hr />
            <label>
            Category : <input value={category} onChange={onCategoryChange} />
            </label>
            <hr />
            <label>
            Description : <input value={description} onChange={onDescriptionChange} />
            </label>
            <hr />
            <button type="submit">{editingId === null
            ? "Add Expense"
            : "Update Expense"}
            </button>
        </form> 
    )

}

export default ExpenseForm