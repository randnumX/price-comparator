import React, { useEffect, useState } from "react";
import { Loader } from 'semantic-ui-react';
import ProductComponent from './ProductComponent';
import { api } from '../services/api';

const HistoryComponent = ({ searchType }) => {
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchItems = async () => {
            try {
                const payload = { type: searchType };
                const data = await api.getHistory(payload);
                setItems(data);
            } catch (error) {
                console.error('Error fetching history:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchItems();
    }, [searchType]);

    const handleAddToTrack = (item) => {
        console.log('Added to track from history:', item);
    }

    if (isLoading) {
        return <Loader active inline='centered' />;
    }

    return <ProductComponent listofItems={items} onAddToTrack={handleAddToTrack} />;
}

export default HistoryComponent;