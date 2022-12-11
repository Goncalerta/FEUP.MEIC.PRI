import { Box, Container, Rating, Typography } from "@mui/material";
import PropTypes from "prop-types";
import StarIcon from "@mui/icons-material/Star";

function SearchResults(props) {
    const { loading, error, data } = props;

    const ERROR_MESSAGE = "An error occurred :(";
    const NO_RESULTS_MESSAGE = "No results found.";

    const renderResult = (book) => (
        <Container key={book.id} sx={{ marginTop: "3em" }}>
            <Typography sx={{ fontSize: 34, margin: "0" }} color="text.secondary" gutterBottom>
                <a href="/book/0">The adventures of this name has to change</a>
            </Typography>
            <Typography sx={{ fontSize: 18, margin: "0" }} color="text.secondary" gutterBottom>
                Authored by Pedro Gonçalo (2001-), Nuno Costa (2001-) and William Deadspear
                (1200-1210)
            </Typography>
            <Typography sx={{ fontSize: 12, margin: "0" }} color="text.secondary" gutterBottom>
                Home Economics, Science, History, Geography, Art, Music, Drama, Physical, Erotic
            </Typography>
            <Typography sx={{ fontSize: 12, margin: "0" }} color="text.secondary" gutterBottom>
                Released on 17/04/2023
            </Typography>
            <Box
                sx={{
                    width: 200,
                    display: "flex",
                    alignItems: "center",
                }}
            >
                <Rating
                    value={4}
                    readOnly
                    precision={0.5}
                    emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
                />
                <Typography
                    sx={{ fontSize: 14, margin: "0", marginLeft: "0.2em", lineHeight: "0.1em" }}
                    color="text.secondary"
                    gutterBottom
                >
                    • 13 ratings
                </Typography>
            </Box>
        </Container>
    );

    return (
        <Container>
            {/* <Typography sx={{ fontSize: 34 }} color="text.secondary" gutterBottom>
                Results
            </Typography> */}
            {loading && <p>Loading...</p>}
            {error && <p>{ERROR_MESSAGE}</p>}
            {!loading && !error && data.length === 0 && <p>{NO_RESULTS_MESSAGE}</p>}
            {!loading && !error && data.map((book) => renderResult(book))}
        </Container>
    );
}

SearchResults.propTypes = {
    loading: PropTypes.bool.isRequired,
    error: PropTypes.bool.isRequired,
    data: PropTypes.array.isRequired /* eslint-disable-line react/forbid-prop-types */,
};

export default SearchResults;
