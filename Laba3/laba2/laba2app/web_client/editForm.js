/**
 * Created by karim on 30.10.16.
 */
import React, { Component } from 'react';

class EditForm extends Component {
    constructor(props) {
        super(props);

        this.state = {
            product: "",
            seller: "",
            customer: "",
            totalPrice: 0,
            amount: 0
        };


        this.onSelectProduct = this.onSelectProduct.bind(this);
        this.onAdd = this.onAdd.bind(this);
        this.onUpdate = this.onUpdate.bind(this);

        this.changeAmount = this.changeAmount.bind(this);
    }

    changeAmount(count) {
        this.setState({
            amount: count,
            totalPrice: count * this.state.product.price
        });
    }

    onAdd() {
        this.props.onAdd(this.state);
    }

    onUpdate() {
        let sale = Object.assign(this.props.sale, this.state);
        this.props.onUpdate(sale);
    }

    componentWillReceiveProps(nextProps) {
        if(nextProps.sale) {
            this.setState({
                product: nextProps.sale.product,
                seller: nextProps.sale.seller,
                customer: nextProps.sale.customer,
                totalPrice: nextProps.sale.totalPrice,
                amount: nextProps.sale.amount
            });
        } else {
            this.setState({
                product: nextProps.products[0],
                seller: nextProps.sellers[0],
                customer: nextProps.customers[0],
                totalPrice: nextProps.products[0] ? +nextProps.products[0].price : 0,
                amount: 1
            });
        }
    }

    onSelectProduct(idProduct) {
        let target = this.props.products.find(p => p._id.$oid === idProduct);
        this.setState({product: target});
    }

    render() {
        let endPrice = this.state.product ? this.state.product.price * this.state.amount : 0;
        let price = this.state.product ? this.state.product.price : 0;
        let product = this.state.product ? this.state.product._id.$oid : "Select...";
        let seller = this.state.seller ? this.state.seller._id.$oid : "Select...";
        let customer = this.state.customer ? this.state.customer._id.$oid : "Select...";

        return (
            <div className="editForm">
                <div className="field">
                    <select name="product" value={product} onChange={(e) => this.onSelectProduct(e.target.value)}>
                        {
                            this.props.products.map((p, i) => {
                                return <option value={p._id.$oid} key={i}>{p.productName}</option>
                            })
                        }
                    </select>
                </div>
                <div className="field">
                    <select name="seller" value={seller} onChange={(e) => this.setState({seller: this.props.sellers.find(s => s._id.$oid === e.target.value)})}>
                        {
                            this.props.sellers.map((s, i) => {
                                return <option value={s._id.$oid} key={i}>{s.firstName}</option>
                            })
                        }
                    </select>
                </div>
                <div className="field">
                    <select name="customer" value={customer} onChange={(e) => this.setState({customer: this.props.customers.find(c => c._id.$oid === e.target.value)})}>
                        {
                            this.props.customers.map((c, i) => {
                                return <option value={c._id.$oid} key={i}>{c.firstName}</option>
                            })
                        }
                    </select>
                </div>
                <div className="field">
                    <span>{price}</span>
                </div>
                <div className="field">
                    <input type="number" min="1" value={this.state.amount} onChange={(e) => this.changeAmount(e.target.value)}/>
                </div>
                <div className="field">
                    <span>{endPrice}</span>
                </div>
                <div className="field">
                    {
                        this.props.sale ?
                            <button onClick={this.onUpdate}>Update</button>
                            :
                            <button onClick={this.onAdd}>Add</button>
                    }
                </div>
            </div>
        );
    }
}

EditForm.PropTypes = {
    sellers: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
    customers: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
    products: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,

    sale: React.PropTypes.object,

    onAdd: React.PropTypes.func.isRequired,
    onUpdate: React.PropTypes.func.isRequired
};

export default EditForm;
