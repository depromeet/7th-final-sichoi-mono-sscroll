import {
  AppBar,
  Box,
  Container,
  createMuiTheme,
  CssBaseline,
  ThemeProvider,
  Toolbar,
  Typography,
  makeStyles,
} from '@material-ui/core';
import { ItemList } from 'app/components/Item';
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

const itemStyles = makeStyles({
  container: {
    paddingLeft: '0',
    paddingRight: '0',
  },
});

interface Props {
  onUpdate: () => void;
}

const View = ({ onUpdate }: Props) => {
  // const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const style = itemStyles();

  onUpdate();
  const prefersDarkMode = true;

  const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode],
  );
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <CssBaseline />
        <Box>
          <AppBar position="static" color="default">
            <Toolbar>
              <Typography variant="h6">쓰끄롤</Typography>
            </Toolbar>
          </AppBar>
          <Container maxWidth="md" className={style.container}>
            <Route path="/:id?" component={ItemList} />
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default View;
