import {
  Box,
  Button,
  Card,
  Collapse,
  makeStyles,
  Typography,
  RootRef,
} from '@material-ui/core';
import { observer } from 'mobx-react';
import React, { useEffect, useState, useCallback, useRef } from 'react';
import { useParams } from 'react-router';
import ItemStore from 'store/item';
import ItemModel from 'store/item/model';
import InfiniteScroll from 'react-infinite-scroller';
import { link } from 'utils';

interface Params {
  id: string;
}

export const ItemList = observer(() => {
  const { id } = useParams<Params>();
  const [hasId, setHasId] = useState(!!id);

  useEffect(() => {
    if (!id) {
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
      hasMore={true}
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
  const [height, setHeight] = useState(500);
  const [expandValue, setExpandValue] = useState(1000);
  const contentBox = useRef();

  const expand = useCallback(() => {
    const currentRef = contentBox.current;
    if (currentRef) {
      const el = currentRef as HTMLElement;
      const maxHeight = el.getBoundingClientRect().height;
      if (height + expandValue >= maxHeight) {
        setHeight(maxHeight);
        setExpaned(true);
      } else {
        setHeight(height + expandValue);
        setExpandValue(expandValue * 2);
      }
    }
    data.read();
  }, [height, expandValue, data]);

  return (
    <Box className={style.box}>
      <Card className={style.card}>
        <Box className={style.contentBox}>
          <Box mb="0.5rem">
            <Typography variant="h6">{item.title}</Typography>
            <Button onClick={() => link(item.id)}>링크 복사하기</Button>
          </Box>
          <Collapse in={expaneded} collapsedHeight={height}>
            <RootRef rootRef={contentBox}>
              <Box dangerouslySetInnerHTML={{ __html: item.content }}></Box>
            </RootRef>
          </Collapse>
        </Box>
        <Collapse in={!expaneded} collapsedHeight={0}>
          <Box>
            <Button className={style.button} onClick={expand}>
              펼치기
            </Button>
          </Box>
        </Collapse>
      </Card>
    </Box>
  );
};
