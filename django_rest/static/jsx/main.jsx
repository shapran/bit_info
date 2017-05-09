var React = require('react');
var ReactDOM = require('react-dom');
var PropTypes = require('prop-types');


var dropDownOnChange = function(change) {
        alert('onChangeForSelect:\noldValue: ' +
                change.oldValue +
                '\nnewValue: '
                + change.newValue);
};

var Dropdown = React.createClass({

    propTypes: {
        id: PropTypes.string.isRequired,
        options: PropTypes.array.isRequired,
        value: PropTypes.oneOfType(
            [
                PropTypes.number,
                PropTypes.string
            ]
        ),
        valueField: PropTypes.string,
        labelField: PropTypes.string,
        onChange: PropTypes.func
    },

    getDefaultProps: function() {
        return {
            value: null,
            valueField: 'value',
            labelField: 'label',
            onChange: null
        };
    },

    getInitialState: function() {
        var selected = this.getSelectedFromProps(this.props);
        return {
            selected: selected
        }
    },

    componentWillReceiveProps: function(nextProps) {
        var selected = this.getSelectedFromProps(nextProps);
        this.setState({
           selected: selected
        });
    },

    getSelectedFromProps(props) {
        var selected;
        if (props.value === null && props.options.length !== 0) {
            selected = props.options[0][props.valueField];
        } else {
            selected = props.value;
        }
        return selected;
    },

    render: function() {
        var self = this;
        var options = self.props.options.map(function(option) {
            return (
                <option key={option[self.props.valueField]} value={option[self.props.valueField]}>
                    {option[self.props.labelField]}
                </option>
            )
        });
        return (
            <div className="col-xs-3">
            <select id={this.props.id}
                    className='form-control'
                    value={this.state.selected}
                    onChange={this.handleChange}>
                {options}
            </select>
            </div>
        )
    },

    handleChange: function(e) {
        if (this.props.onChange) {
            var change = {
              oldValue: this.state.selected,
              newValue: e.target.value
            }
            this.props.onChange(change);
        }
        this.setState({selected: e.target.value});
    }

});

var options = [
        {
            description: 'This is option A',
            code: 'a'
        },
        {
            description: 'This is option B',
            code: 'b'
        },
        {
            description: 'This is option C',
            code: 'c'
        },
        {
            description: 'This is option D',
            code: 'd'
        }
    ];



// ReactDOM.render(<Dropdown list={colours} selected={colours[0]} />, document.getElementById("example"));
ReactDOM.render(
        <Dropdown id='myDropdown'
                  options={options}
                  value='b'
                  labelField='description'
                  valueField='code'
                  onChange={dropDownOnChange}/>,
        document.getElementById('example'));