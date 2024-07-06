import React, { useState } from 'react';
import { Input, Button, Dropdown, Form } from 'semantic-ui-react';
import './SearchComponent.css';

const SearchComponent = ({ onSearch, searchType }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [flightFrom, setFlightFrom] = useState('');
    const [flightTo, setFlightTo] = useState('');
    const [flightDate, setFlightDate] = useState('');

    const handleInputChange = (event) => {
        setSearchTerm(event.target.value);
    }

    const handleFlightFromChange = (_, { value }) => {
        setFlightFrom(value);
    }

    const handleFlightToChange = (_, { value }) => {
        setFlightTo(value);
    }

    const handleFlightDateChange = (event) => {
        setFlightDate(event.target.value);
    }

    const handleSearch = (event) => {
        event.preventDefault();
        if (searchType === 'shopping') {
            onSearch(searchTerm);
        } else if (searchType === 'flights') {
            const searchData = {
                from: flightFrom,
                to: flightTo,
                date: flightDate
            };
            onSearch(searchData);
        }
    }

    const shoppingPlaceholder = 'Search for products...';
    const flightPlaceholder = 'Search for flights...';

    return (
        <div className="ui search-container">
            <Form onSubmit={handleSearch} className="ui center aligned form">
                {searchType === 'shopping' ? (
                    <div className="field">
                        <div className="ui action input">
                            <Input
                                fluid
                                type="text"
                                placeholder={shoppingPlaceholder}
                                value={searchTerm}
                                onChange={handleInputChange}
                                style={{ minWidth: "20rem" }}
                                icon='search'
                                iconPosition='left'
                            />
                            <Button primary type="submit">Search</Button>
                        </div>
                    </div>
                ) : searchType === 'flights' ? (
                    <div className="fields">
                        <div className="field" style={{ width: '45%' }}>
                            <Dropdown
                                placeholder='From'
                                fluid
                                selection
                                options={[ /* Your flight options here */ ]}
                                onChange={handleFlightFromChange}
                                value={flightFrom}
                            />
                        </div>
                        <div className="field" style={{ width: '45%' }}>
                            <Dropdown
                                placeholder='To'
                                fluid
                                selection
                                options={[ /* Your flight options here */ ]}
                                onChange={handleFlightToChange}
                                value={flightTo}
                            />
                        </div>
                        <div className="field" style={{ width: '25%' }}>
                            <Input
                                fluid
                                type="date"
                                placeholder='Date'
                                value={flightDate}
                                onChange={handleFlightDateChange}
                            />
                        </div>
                        <Button primary type="submit" style={{ width: '20%' }}>Search</Button>
                    </div>
                ) : null}
            </Form>
        </div>
    );
}

export default SearchComponent;
