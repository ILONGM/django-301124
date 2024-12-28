//importe le CSS
const link = document.createElement('link');
link.rel='stylesheet';
link.href = './static/monapp/css/style.css';
document.head.appendChild(link);

let stocks = [];

// fetch portfolios 1 current open positions
async function fetchPortfolios() {
  try {
    const response = await fetch('/portfolios/1/'); // Remplacez 1 par l'ID du portefeuille
    const data = await response.json();
    //injecte dans la variable stocks mon portfolios
    stocks.push(...data.portfolios); // Remplit stocks avec les données reçues
    createPortfolioTable(); // Crée le tableau après avoir les données

  } catch (error) {
    console.error('Erreur lors de la récupération des portfolios:', error);
  }
}
fetchPortfolios();


const formatter = new Intl.NumberFormat('fr-FR', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

function formatNumber(number) {
  return formatter.format(number);
}

function calculatePortfolioTotal() {
  return stocks.reduce((total, stock) => total + (stock.shares * stock.currentPrice), 0);
}
function calculateInvestedAtCostTotal() {
  return stocks.reduce((total, stock) => total + (stock.net_cost), 0);
}


// Crée le tableau avec mes actions 
function createPortfolioTable() {
  const tableHTML = `
    <div class="container">
      <div class="portfolio-header">
        <h1>Mon Yolofolio d'Investissement</h1>
      </div>
      <div class="portfolio-table">
        <table>
          <thead>
            <tr>
              <th>Action</th>
              <th>Marché et Horaire</th>
              <th>Nombre d'Actions</th>
              <th>At cost </th>
              <th>Prix Actuel</th>
              <th>Valeur Totale</th>
            </tr>
          </thead>
          <tbody id="stockTableBody">
            ${stocks.map(stock => `
              <tr>
                <td>
                  <div class="stock-info">
                    <img src="${stock.logo}" alt="${stock.name} logo" class="stock-logo">
                    <div>
                      <div class="stock-name">${stock.name}</div>
                      <div class="stock-ticker">${stock.ticker}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="market-info">
                    <span class="market-name">${stock.market}</span>
                  </div>
                </td>
                <td>
                  <span class="shares-display">${stock.shares}</span>
                </td>

                <td>
                    <span class="invested_at_cost">${formatNumber(stock.net_cost)}</span>
                </td>

                <td class="stock-price" data-ticker="${stock.ticker}">Chargement...</td>
                <td class="stock-total" data-ticker="${stock.ticker}">Chargement...</td>
              </tr>
            `).join('')}

            <tr class="portfolio-total">
              <td colspan="2"><strong>Total du Portfolio</strong></td>
              <td colspan="1">
              <td id="At_cost_total" >Chargement...</td>

              <td colspan="1">
              </td>
              <td id="portfolioTotal" class="portfolio-total-value">Chargement...</td>
            </tr>

          </tbody>
        </table>
      </div>
    </div>
  `;

  document.querySelector('#app').innerHTML = tableHTML;
}

// update stock price function
async function updateStockPrices() {
  try {
    for (const stock of stocks) {
      //const data = await getStockQuote(stock.ticker);
      // remettre la ligne au dessus pour l'appel API
      const data = 123
      if (data) {
        stock.currentPrice = data;
//        stock.currentPrice = data.regularMarketPrice;

        const priceElement = document.querySelector(`.stock-price[data-ticker="${stock.ticker}"]`);
        const totalElement = document.querySelector(`.stock-total[data-ticker="${stock.ticker}"]`);

        if (priceElement && totalElement) {
          priceElement.textContent = formatNumber(stock.currentPrice);
          const total = stock.shares * stock.currentPrice;
          totalElement.textContent = formatNumber(total);
        }
      }
    }

    // Mise à jour du total du portfolio
    const portfolioTotalElement = document.getElementById('portfolioTotal');
    if (portfolioTotalElement) {
      portfolioTotalElement.textContent = formatNumber(calculatePortfolioTotal());
    }
    // Mise à jour du total at cost
    const portfolioTotalElement2 = document.getElementById('At_cost_total');
    if (portfolioTotalElement2) {
      portfolioTotalElement2.textContent = formatNumber(calculateInvestedAtCostTotal());
    }


  } catch (error) {
    console.error('Erreur lors de la mise à jour des prix:', error);
  }
}



async function getStockQuote(ticker) {
  const url = `https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes?ticker=${ticker}`;

  const options = {
    method: 'GET',
    headers: {
      'X-Rapidapi-Key': '51c5eb891fmshbd596b70f1034c1p19c22ajsn2493ed1108e3',
      'X-Rapidapi-Host': 'yahoo-finance15.p.rapidapi.com',
    },
  };

  try {
    const response = await fetch(url, options);
    const data = await response.json();
    console.log(data)
    //if (data && data.body[0]) {
    return data.body[0].regularMarketPrice;
    //} else {
    // console.error(`Aucune donnée trouvée pour ${ticker}`);
    //  return null;
    //}
    
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
  }
}

// Exemple d'appel
//getStockQuote('TSLA'); // Remplacez 'TSLA' par un autre symbole boursier si besoin



// Initialisation
createPortfolioTable();

// Mise à jour des prix toutes les 5 secondes
setInterval(updateStockPrices, 5000);
updateStockPrices();
