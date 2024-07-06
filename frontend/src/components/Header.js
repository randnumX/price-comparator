import React, { useState } from 'react';
import { Menu, Container, Radio, Icon } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

const Header = ({ searchType, onSearchTypeChange }) => {
    const [currentSearchType, setCurrentSearchType] = useState(searchType);

    const handleSearchTypeChange = () => {
        const newSearchType = currentSearchType === 'shopping' ? 'flights' : 'shopping';
        setCurrentSearchType(newSearchType);
        onSearchTypeChange(newSearchType);
    }

    return (
        <Menu fixed="top" inverted>
            <Container>
                <Menu.Item as={Link} to="/" header>
                    <strong>Price Comparator</strong>
                </Menu.Item>
                <Menu.Item style={{  textAlign: 'center' }}>
                    {currentSearchType === 'shopping' ? (
                        <>
                            <Icon name='plane' color='white' />
                        </>
                    ) : (
                        <>
                            <Icon name='shopping cart' color='white' />
                        </>
                    )}
                </Menu.Item>
                <Menu.Item position="right">
                    <Radio
                        toggle
                        label={currentSearchType === 'shopping' ? <Icon name='shopping cart' color='white' /> : <Icon name='plane' color='white' />}
                        checked={currentSearchType === 'shopping'}
                        onChange={handleSearchTypeChange}
                    />
                </Menu.Item>
            </Container>
        </Menu>
    );
};

export default Header;
