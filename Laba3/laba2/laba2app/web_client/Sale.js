/**
 * Created by karim on 20.10.16.
 */

import React from 'react';

const Sale = (props) => {
    let date = new Date(+props.sale.date.$date);
    let dateString = date.getDate() + "." + (date.getMonth()+1) + "." + date.getFullYear();
    return (
        <div className="sale">
            <div className="column">{props.sale.product.productName}</div>
            <div className="column">{props.sale.seller.firstName}</div>
            <div className="column">{props.sale.customer.firstName}</div>
            <div className="column">{props.sale.product.price}</div>
            <div className="column">{props.sale.amount}</div>
            <div className="column">{props.sale.totalPrice}</div>
            <div className="column">{dateString}</div>
            <div className="column">
                <button className="remove-btn" onClick={(e) => props.removeSale(props.sale)}>delete</button>
                <button className="update-btn" onClick={(e) => props.onSelect(props.sale)}>Update</button>
            </div>
        </div>
    );
};

Sale.PropTypes = {
    sale: React.PropTypes.object.isRequired,

    onSelect: React.PropTypes.func.isRequired,
    removeSale: React.PropTypes.func.isRequired
};

export default Sale;