function ExpenseItem({ category, amount, description }) {
  return (
    <li>
      category: {category} - amount: {amount}€ - description: {description}
    </li>
  );
}

export default ExpenseItem;



