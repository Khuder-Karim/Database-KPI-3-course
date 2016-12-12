/**
 * Created by karim on 05.12.16.
 */
import React from 'react';

const FindBlock = (props) => {
    return (
        <select value="Select..." onChange={e => props.onSelect(e.target.value)}>
            {
                props.products.map((p, i) => {
                    return <option value={p._id.$oid} key={i}>{p.productName}</option>
                })
            }
        </select>
    );
};

FindBlock.PropTypes = {
    products: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
    onSelect: React.PropTypes.func.isRequired
};

export default FindBlock;


