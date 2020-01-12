import { Box, Button, Card, Collapse, makeStyles, Typography } from '@material-ui/core';
import { observer } from 'mobx-react';
import React, { useState } from 'react';
import InfiniteScroll from 'react-infinite-scroller';
import ItemStore from 'store/item';
import ItemModel from 'store/item/model';

export const ItemList: React.FC = observer(() => {
  const store = ItemStore;

  return (
    <InfiniteScroll
      loader={
        <div className="loader" key={0}>
          Loading ...
        </div>
      }
      loadMore={store.fetch}
      hasMore={!store.isLoading}
      key={Math.floor(Math.random() * 10000)}
    >
      {store.itemList.map(item => (
        <Item data={item} key={item.id}></Item>
      ))}
    </InfiniteScroll>
  );
});

const itemStyles = makeStyles({
  box: {
    marginTop: '1rem',
  },
  card: {
    padding: '1rem',
  },
  contentBox: {
    overflow: 'hidden',
  },
  button: {
    width: '100%',
    marginTop: '1rem',
  },
});

interface IProps {
  data: ItemModel;
  key: number;
}

export const Item: React.FC<IProps> = props => {
  const item = props.data;
  const style = itemStyles();

  const [expaneded, setExpaned] = useState(false);

  return (
    <Box className={style.box}>
      <Card className={style.card}>
        <Collapse in={expaneded} collapsedHeight={500}>
          <Box className={style.contentBox}>
            <Box>
              <Typography variant="h6">{item.title}</Typography>
            </Box>
            <Box dangerouslySetInnerHTML={{ __html: item.content }}></Box>
          </Box>
        </Collapse>
        <Collapse in={!expaneded} collapsedHeight={0}>
          <Box>
            <Button
              className={style.button}
              onClick={() => {
                setExpaned(true);
              }}
            >
              펼치기
            </Button>
          </Box>
        </Collapse>
      </Card>
    </Box>
  );
};
