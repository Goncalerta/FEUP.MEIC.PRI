import Paper from "@mui/material/Paper";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import PropTypes from "prop-types";

function SearchBar(props) {
    return (
        <Paper sx={{ p: "2px 4px", display: "flex", alignItems: "center", width: "100%" }}>
            <InputBase
                sx={{ ml: 1, flex: 1 }}
                placeholder="Search..."
                id="searchBar"
                inputProps={{ "aria-label": "search" }}
                onKeyPress={(ev) => {
                    if (ev.key === "Enter") {
                        ev.preventDefault();
                        props.onSearch(ev.target.value);
                    }
                }}
            />
            <IconButton
                type="button"
                sx={{ p: "10px" }}
                aria-label="search"
                onClick={() => {
                    props.onSearch(document.getElementById("searchBar").value);
                }}
            >
                <SearchIcon />
            </IconButton>
        </Paper>
    );
}

SearchBar.propTypes = {
    onSearch: PropTypes.func.isRequired,
};

export default SearchBar;
