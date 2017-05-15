var React = require('react');
var ReactDOM = require('react-dom');
var PropTypes = require('prop-types');

import axios from 'axios';
import jquery from 'jquery';

var jQuery = jquery;


var Dropdown;
var Dropdown = React.createClass({

  // Get cookie data
  getCookie: function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
  },

  // Fills select list and fetches last market data for all currencies
  getInitialState: function () {
    return { info: [{name: 'All', symbol: 'all_symbols'}],
             table_data: []};
  },

  componentDidMount: function () {
    var csrf_token = this.getCookie('csrftoken');

        var config = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrf_token
            }
        };

        var base_url = 'http://127.0.0.1:8000/api/v1/simple/?page=';
        var temp = [{name: 'All', symbol: 'all_symbols'}];
        var total_pages = 1;
        var _this = this;

        axios.get(base_url + total_pages, config).then(function (res) {
            total_pages = res.data.total_pages;

            var promises = [];
            for (var i = 1; i <= total_pages; i++) {
                promises.push(axios.get(base_url + i, config))
            }
            axios.all(promises).then(function (results) {
                results.forEach(function (response) {
                    var item = {name: "zzz", symbol: "qqq"};
                    temp.push.apply(temp, response.data.results);
                    _this.setState({info: temp});
                    _this.getLastData();
                })
            })
        }).catch(function (error) {
                console.log('Data fetch error: ', error);
      });
    },

  // Fetch all market data related with chosen symbol
  getSymbolData: function(symb)   {
    var csrf_token = this.getCookie('csrftoken');

    var config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrf_token
        }
    };

    var base_url = 'http://127.0.0.1:8000/api/v1/symbols/';
    var t_data = [];
    var _this = this;

    axios.get(base_url + symb, config).then(function (res) {
            var detail_pages = res.data.coins;

            var promises = [];
            for (var i = 1; i < detail_pages.length; i++) {
                promises.push(axios.get(detail_pages[i], config))
            }
            axios.all(promises).then(function (results) {
                results.forEach(function (response) {
                    t_data.push(response.data);
                    _this.setState({table_data: t_data});
                })
            })
        }).catch(function (error) {
                console.log('Data fetch error: ', error);
      });
  },

  // Get latest (filter by update_date field) market data
  getLastData: function()   {
    var csrf_token = this.getCookie('csrftoken');

    var config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrf_token
        },
        params: {all: 'true', page: 1}
    };

    var base_url = 'http://127.0.0.1:8000/api/v1/coins/';
    var temp = [{name: 'All', symbol: 'all_symbols'}];
    var total_pages = 1;
    var _this = this;

    axios.get(base_url, config).then(function (res) {
        total_pages = res.data.count;
        var promises = [];

        for (var i = 1; i <= 1; i++) {
            var config = {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrf_token
                },
                params: {all: 'true', page_size: total_pages}
            };
            promises.push(axios.get(base_url, config))
        }
        axios.all(promises).then(function (results) {
            results.forEach(function (response) {

                temp.push.apply(temp, response.data.results);
                _this.setState({table_data: temp});
            })
        })
        }).catch(function (error) {
            console.log('Data fetch error: ', error);
    });
  },

  // Handle select switch option
  handleChange(event) {
    var symb = event.target.value.toUpperCase();
    console.log(symb);
    if (symb == "ALL_SYMBOLS")  {
        this.getLastData();
    } else  {
       this.getSymbolData(symb);
    }
  },

  render: function() {

    var symbols = this.state.info.map(function (symbol) {
       return (
           <option key={symbol.symbol + symbol.name} value={symbol.symbol}>
               {symbol.name}
           </option>
       )
    });

    var rows = this.state.table_data.map(function (row) {
       return (
           <tr key={row.id}>
                <td>{ row.name }</td>
                <td>{ row.symb }</td>
                <td>{ row.market_cap }</td>
                <td>{ row.price }</td>
                <td>{ row.supply }</td>
                <td>{ row.volume }</td>
                <td>{ row.hour_prc }</td>
                <td>{ row.day_prc }</td>
                <td>{ row.week_prc }</td>
           </tr>
       )
    });

    return (
        <div className="table_wrapper">
            <div className="select_block">
                <select onChange={this.handleChange}>{symbols}</select>
            </div>
            <div className="table_block">
            <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Symbol</th>
                    <th>Market Cap</th>
                    <th>Price</th>
                    <th>Circulating Supply</th>
                    <th>Volume (24h)</th>
                    <th>1h, %</th>
                    <th>24h, %</th>
                    <th>7d, %</th>
                  </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            </div>
        </div>
    );
  }
});

ReactDOM.render(
        <Dropdown id='dataFilter'/>,
        document.getElementById('react_wrapper'));