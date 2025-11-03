// ==========================
// 📘 Digital Library JS Bundle
// ==========================

// Utility — show a toast alert
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast-message ${type}`;
  toast.innerText = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 100);
  setTimeout(() => toast.classList.remove('show'), 3000);
  setTimeout(() => toast.remove(), 3500);
}

// ==========================
// 🔍 Search Books (Student)
// ==========================
$(document).on('input', '#search', function() {
  const q = $(this).val().toLowerCase();
  $('.book-item').each(function() {
    const text = $(this).text().toLowerCase();
    $(this).toggle(text.includes(q));
  });
});

// ==========================
// 📚 Borrow Book via AJAX
// ==========================
$(document).on('click', '.borrow-btn', function() {
  const id = $(this).data('id');
  $.post(`/borrow/book/${id}`, {}, function(res) {
    if (res.message) showToast(res.message, 'success');
    if (res.error) showToast(res.error, 'error');
    setTimeout(() => location.reload(), 2000);
  });
});


// ==========================
// 🤖 Chatbot Interaction
// ==========================
$(document).on('keypress', '#chat-input', function(e) {
  if (e.which === 13) {
    const msg = $(this).val().trim();
    if (!msg) return;
    $(this).val('');
    $('#chat-body').append(`<div class='user-msg'>${msg}</div>`);
    $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight);
    
    $.ajax({
      url: '/chatbot/ask',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ message: msg }),
      success: function(data) {
        $('#chat-body').append(`<div class='bot-msg'>${data.reply}</div>`);
        $('#chat-body').scrollTop($('#chat-body')[0].scrollHeight);
      },
      error: function() {
        $('#chat-body').append(`<div class='bot-msg text-danger'>⚠️ Network error.</div>`);
      }
    });
  }
});

// ==========================
// 🧩 Admin Panel Controls
// ==========================
function loadBooks() {
  $.get('/books/list', function(data) {
    const table = $('#book-table');
    if (!table.length) return; // only run if admin page
    table.empty();
    data.forEach(b => {
      table.append(`
        <tr>
          <td>${b.id}</td>
          <td>${b.title}</td>
          <td>${b.author}</td>
          <td>${b.category_name}</td>
          <td>${b.available_copies}</td>
          <td>
            <button class='btn btn-sm btn-danger' onclick='deleteBook(${b.id})'>Delete</button>
          </td>
        </tr>`);
    });
  });
}

function deleteBook(id) {
  if (confirm('Delete this book?')) {
    $.ajax({
      url: '/books/delete/' + id,
      type: 'DELETE',
      success: function() {
        showToast('Book deleted successfully', 'success');
        loadBooks();
      },
      error: function() {
        showToast('Error deleting book', 'error');
      }
    });
  }
}

$(document).on('click', '#addBookBtn', function() {
  const title = prompt('Book Title:');
  const author = prompt('Author:');
  const category_id = prompt('Category ID:');
  const copies = prompt('Available copies:', 1);
  
  if (title && author && category_id) {
    $.ajax({
      url: '/books/add',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ title, author, category_id, available_copies: copies }),
      success: function() {
        showToast('Book added successfully!', 'success');
        loadBooks();
      },
      error: function() {
        showToast('Error adding book', 'error');
      }
    });
  }
});

// Load books automatically on admin page
$(document).ready(loadBooks);

// ==========================
// ✨ Toast Style
// ==========================
const style = document.createElement('style');
style.innerHTML = `
.toast-message {
  position: fixed;
  top: 20px;
  right: -300px;
  background: #333;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  opacity: 0;
  transition: all 0.5s ease;
  z-index: 1000;
}
.toast-message.show {
  right: 20px;
  opacity: 1;
}
.toast-message.success { background: #198754; }
.toast-message.error { background: #dc3545; }
.toast-message.info { background: #0d6efd; }
`;
document.head.appendChild(style);
