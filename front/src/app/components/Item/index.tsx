import { Box, Button, Card, Collapse, makeStyles, Typography } from '@material-ui/core';
import { observer } from 'mobx-react';
import React, { useEffect, useState } from 'react';
import InfiniteScroll from 'react-infinite-scroller';
import { useParams } from 'react-router';
import ItemStore from 'store/item';
import ItemModel from 'store/item/model';

interface Params {
  id: string;
}

export const ItemList = observer(() => {
  const { id } = useParams<Params>();
  const [hasId, setHasId] = useState(!!id);

  useEffect(() => {
    if (!id) {
      console.log('what');
      return;
    }

    ItemStore.fetchById(id);
    setHasId(false);
  }, [id]);

  return hasId ? (
    <></>
  ) : (
    <InfiniteScroll
      loader={
        <div className="loader" key={0}>
          Loading ...
        </div>
      }
      loadMore={ItemStore.fetch}
      hasMore={!ItemStore.isLoading}
      key={0}
    >
      {ItemStore.itemList.map(item => (
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

interface Props {
  data: ItemModel;
  key: number;
}

export const Item = ({ data, key }: Props) => {
  const item = data;
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
                data.read();
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
