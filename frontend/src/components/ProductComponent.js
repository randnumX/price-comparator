import React, { useState } from "react";
import { Grid, Card, Icon, Button } from "semantic-ui-react";
import { api } from '../services/api'; 

const ProductComponent = ({ listofItems, onAddToTrack }) => {
    const [clickedProducts, setClickedProducts] = useState({});

    const handleAddToTrack = async (product) => {
        try {
            const isCurrentlyClicked = clickedProducts[product.id];
            console.log(product)

            setClickedProducts(prevState => ({
                ...prevState,
                [product.id]: !isCurrentlyClicked
            }));

            if (isCurrentlyClicked) {
                await api.removeTrackedItem(product);
            } else {
                await api.addtrackItem(product);
            }

            if (onAddToTrack) {
                onAddToTrack(product);
            }

            setTimeout(() => {
                setClickedProducts(prevState => ({
                    ...prevState,
                    [product.id]: isCurrentlyClicked  
                }));
            }, 1000); 
        } catch (error) {
            console.error('Error adding product to track:', error);
        }
    };

    const renderList = listofItems.map((product) => {
        const { id, image_url, price, url, name } = product;
        const isClicked = clickedProducts[product.id];

        return (
            <Grid.Column key={id}>
                <Card>
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', maxHeight: '200px', maxWidth: '100%', overflow: 'hidden' }}>
                        <img src={image_url} style={{ maxHeight: '100%', maxWidth: '100%' }} alt={name} />
                    </div>
                    <Card.Content>
                        <Card.Header style={{ fontSize: '14px', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitBoxOrient: 'vertical', WebkitLineClamp: 4 }}>{name}</Card.Header>
                        <Card.Meta>
                            <span className="price" style={{ fontSize: '16px', color: 'darkblue' }}>
                                <Icon name="rupee sign" />
                                {price}
                            </span>
                        </Card.Meta>
                    </Card.Content>
                    <Card.Content extra>
                        <div className='ui two buttons'>
                            <Button basic color='blue' as='a' href={url} target="_blank" rel="noopener noreferrer">
                                <Icon name='shop' /> View on Store
                            </Button>
                            <Button 
                                basic 
                                color= {isClicked ?  'red' : 'green'}
                                onClick={() => handleAddToTrack(product)}
                                className={isClicked ? 'clicked' : ''}
                            >
                                {isClicked ?  <><Icon name='minus' /> Remove</> : <><Icon name='plus' /> Add to Track</>}
                            </Button>
                        </div>
                    </Card.Content>
                </Card>
            </Grid.Column>
        );
    });

    return (
        <Grid columns={4} doubling stackable>
            {renderList}
        </Grid>
    );
};

export default ProductComponent;
