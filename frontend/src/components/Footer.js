import React from "react";
import { Container, Segment, Icon } from "semantic-ui-react";
import "./Footer.css"; // Import your CSS file for custom styling

const Footer = () => {
    return (
        <Segment inverted vertical className="footer">
            <Container>
                <div className="footer-content">
                    <p>Copyright © {new Date().getFullYear()}</p>
                    <p>
                        View source on{" "}
                        <a
                            href="https://github.com/"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <Icon name="github" /> GitHub
                        </a>
                    </p>
                </div>
            </Container>
        </Segment>
    );
};

export default Footer;
