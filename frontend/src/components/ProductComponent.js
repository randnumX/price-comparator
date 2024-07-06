import React from "react";
import { Grid, Card, Image, Icon, Button } from "semantic-ui-react";

const ProductComponent = ({ listofItems, onAddToTrack }) => {
    const renderList = listofItems.map((product) => {
        const { id, title, image, price, category } = product;
        return (
            <Grid.Column key={id}>
                <Card>
                    <Image src={image} wrapped ui={false} />
                    <Card.Content>
                        <Card.Header>{title}</Card.Header>
                        <Card.Meta>
                            <span className="price">
                                <Icon name="rupee sign" />
                                {price}
                            </span>
                        </Card.Meta>
                        <Card.Description>{category}</Card.Description>
                    </Card.Content>
                    <Card.Content extra>
                        <div className='ui two buttons'>
                            <Button basic color='blue' as='a' href="https://google.com" target="_blank" rel="noopener noreferrer">
                                <Icon name='shop' /> View on Store
                            </Button>
                            <Button basic color='green' onClick={() => onAddToTrack(product)}>
                                <Icon name='plus' /> Add to Track
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