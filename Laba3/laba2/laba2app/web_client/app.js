/**
 * Created by karim on 17.10.16.
 */
import React, {Component} from 'react';
import ReactDOM from 'react-dom';

import EditForm from './editForm';
import Sale from './Sale';
import FindBlock from './FindBlock';

class MainComponent extends Component {
    constructor(props) {
        super(props);

        this.state = {
            sales: [],
            sellers: [],
            customers: [],
            products: [],
            selectedSale: ""
        };

        this.COLUMNS = [
            "Product",
            "Seller",
            "Customer",
            "Price",
            "Amount",
            "TotalPrice",
            "Date",
            "Comand"
        ];

        this.onSelectSale = this.onSelectSale.bind(this);
        this.onRemove = this.onRemove.bind(this);
        this.onAddSale = this.onAddSale.bind(this);
        this.onUpdateSale = this.onUpdateSale.bind(this);

        this.findSales = this.findSales.bind(this);

        this.loadCustomers = this.loadCustomers.bind(this);
        this.loadSales = this.loadSales.bind(this);
        this.loadSellers = this.loadSellers.bind(this);
        this.loadProducts = this.loadProducts.bind(this);

        this.restore = this.restore.bind(this);
    }
    loadSellers() {
        fetch('/sellers').then(response => response.json()).then(response => this.setState({sellers: response}));
    }
    loadSales() {
        fetch('/sale').then(response => response.json()).then(response => this.setState({sales: response}));
    }
    loadCustomers() {
        fetch('/customer').then(response => response.json()).then(response => this.setState({customers: response}));
    }
    loadProducts() {
        fetch('/product').then(response => response.json()).then(response => this.setState({products: response}));
    }

    onAddSale(sale) {
        fetch('/sale/add', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sale)
        })
            .then(response => response.json())
            .then(response => {
                this.state.sales.push(response);
                this.setState({sales: this.state.sales});
            })
        ;
    }

    onSelectSale(sale) {
        this.setState({selectedSale: sale});
    }

    onRemove(sale) {
        fetch('/sale/remove', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sale)
        })
            .then(() => {
                let index = this.state.sales.map(s => s._id.$oid).indexOf(sale._id.$oid);
                this.state.sales.splice(index, 1);
                this.setState({sales: this.state.sales});
            })
            .catch(e => console.error(e))
        ;
    }

    onUpdateSale(sale) {
        fetch('/sale/update', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sale)
        })
            .then(response => response.json())
            .then(response => {
                let index = this.state.sales.map(s => s._id.$oid).indexOf(sale._id.$oid);
                this.state.sales.splice(index, 1, response);
                this.setState({sales: this.state.sales, selectedSale: ""});
            })
            .catch(e => console.error(e))
        ;
    }

    restore() {
        fetch('/restore', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
            .then(() => {
                this.loadProducts();
                this.loadCustomers();
                this.loadSellers();
                this.loadSales();
            })
            .catch(e => console.error(e))
        ;
    }

    componentDidMount() {
        this.loadProducts();
        this.loadCustomers();
        this.loadSellers();
        this.loadSales();
    }

    findSales(idProduct) {
        console.log(idProduct);
        fetch('/sale/find', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({idProduct: idProduct})
        })
            .then(response => response.json())
            .then(response => {
                this.setState({ sales: response });
            })
            .catch(e => console.error(e))
        ;
    }

    render() {
        return (
            <div className="container">
                <FindBlock products={this.state.products} onSelect={this.findSales}/>
                <EditForm
                    sellers={this.state.sellers}
                    customers={this.state.customers}
                    products={this.state.products}
                    onAdd={this.onAddSale}
                    onUpdate={this.onUpdateSale}
                    sale={this.state.selectedSale}
                />
                <div className="table">
                    <div className="table__header">
                        {
                            this.COLUMNS.map((c, i) => {
                                return <div className="column" key={i}><span>{c}</span></div>
                            })
                        }
                    </div>
                    {
                        this.state.sales.map((s, i) => {
                            return <Sale key={i} sale={s} removeSale={this.onRemove} onSelect={this.onSelectSale}/>
                        })
                    }
                </div>

                <button className="restore-btn" onClick={(e) => this.restore()}>Restore</button>
            </div>
        );
    }
}

ReactDOM.render(<MainComponent/>, document.getElementById('app'));