import React, { useState } from 'react';
import { Tab, Loader } from 'semantic-ui-react';
import SearchComponent from './SearchComponent';
import HistoryComponent from './HistoryComponent';
import ProductComponent from './ProductComponent';
import { api } from '../services/api';

const HomeComponent = ({ searchType }) => {
    const [activeIndex, setActiveIndex] = useState(1);
    const [searchResults, setSearchResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async (searchTerm) => {
        try {
            setSearchResults([]);
            setActiveIndex(0);
            setIsLoading(true);
            const payload = { name: searchTerm, type: searchType };
            const data = await api.scrape(payload);
            setSearchResults(data);
        } catch (error) {
            console.error('Error fetching search results:', error);
        } finally {
            setIsLoading(false);
        }
    }

    const handleAddToTrack = (item) => {
        console.log('Added to track:', item);
    }

    const panes = [
        {
            menuItem: 'Search', render: () => (
                <Tab.Pane style={{ minHeight: '70vh', display: 'flex', justifyContent: 'center', alignItems: 'center', paddingBottom: '75px', background: 'whitesmoke' }}>
                    {isLoading ? (
                        <Loader active inline='centered' />
                    ) : searchResults.length === 0 ? (
                        <h3 className='center'>Please Search to see some results here...</h3>
                    ) : (
                        <ProductComponent listofItems={searchResults} onAddToTrack={handleAddToTrack} />
                    )}
                </Tab.Pane>
            )
        },
        {
            menuItem: 'Tracked Items', render: () => (
                <Tab.Pane style={{ minHeight: '70vh', paddingBottom: '80px', background: 'whitesmoke' }}>
                    <HistoryComponent searchType={searchType} />
                </Tab.Pane>
            )
        }
    ];

    return (
        <div className="ui container">
            <SearchComponent onSearch={handleSearch} searchType={searchType} />
            <Tab panes={panes} activeIndex={activeIndex} onTabChange={(e, { activeIndex }) => setActiveIndex(activeIndex)} />
            <style jsx>{`
  
      `}</style>
        </div>
    );
}

export default HomeComponent;