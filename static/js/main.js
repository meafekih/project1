

// تحميل قائمة المنتجات عند تحميل الصفحة
window.onload = () => {
    fetchProducts();
  };
  
  
  async function fetchProducts() {
    const response = await fetch('/api/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        query: `
          query {
            allProducts {
              id
              name
              description
              price
            }
          }
        `,
      }),
    });
    const { data } = await response.json();
    const productList = document.getElementById('product-list');
  
    data.allProducts.forEach((product) => {
      const item = document.createElement('li');
      item.textContent = `${product.name} - ${product.price}$`;
      productList.appendChild(item);
    });
  }
  
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  



  //










