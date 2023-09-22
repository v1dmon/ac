# ac

Converts a(n) (a)symmetric trace file to a workload file for the [wgen](https://github.com/v1dmon/wgen) generator.

### Trace file

```
0.162509111929321
0.129387377423254
0.0964237845624633
0.0882911681301054
0.0855407482603705
0.0968362671378106
0.0931622402556432
0.0897799057381511
0.0916050931083065
0.0762924913286654
...
```

### Workload file

```yml
expected:
  duration: 1m
  requests: 34187
workload:
- api: customers_get_all
  rate: 706/s
- api: index_get
  rate: 638/s
- api: tags_get_all
  rate: 643/s
- api: tags_get_all
  rate: 596/s
- api: customers_get_all
  rate: 588/s
...
```

## Usage

```
usage: ac [-h] {cut,zip,gen} ...
usage: ac cut [-h] [-i FILE] [-o FILE] -t TIME
usage: ac zip [-h] [-i FILE] [-o FILE] -t TIME
usage: ac gen [-h] [-i FILE] [-o FILE] [-r SEED] (-a APIs | -A APIs [APIs ...])
```

## Flags

### `cut` command

#### `-i` file *[default `stdin`]*

Filesystem path to the input trace file.
If not passed, `stdin` is used.

#### `-o` file *[default `stdout`]*

Filesystem path for the generated trace.
If not passed, `stdout` is used.

#### `-t` time *[required]*

Time value to extract from the input trace.
Should be passed as a time string: `20s`, `1h`, `1m`, `1d20m13s`, ...\
**NOTE** Cannot be less than or equal to zero.

### `zip` command

#### `-i` file *[default `stdin`]*

Filesystem path to the input trace file.
If not passed, `stdin` is used.

#### `-o` file *[default `stdout`]*

Filesystem path for the generated trace.
If not passed, `stdout` is used.

#### `-t` time *[required]*

Specifies the time at which to compress the input trace.
The zip between actual and compressed time is applies uniformly in order to preserve any asymmetries in the input trace.
Should be passed as a time string: `20s`, `1h`, `1m`, `1d20m13s`, ...\
**NOTE** Cannot be less than or equal to zero.

### `gen` command

#### `-i` file *[default `stdin`]*

Filesystem path to the input trace file.
If not passed, `stdin` is used.

#### `-o` file *[default `stdout`]*

Filesystem path for the generated trace.
If not passed, `stdout` is used.

#### `-r` seed

Seed number used to randomly select APIs during workload generation.
If not passed, APIs are iterated and selected the given order.

#### `-a` apispec *[required]*

Filesystem path to the input [aspispec](https://github.com/v1dmon/wgen) file.\
If not passed, `-A` flag must be used instead.

#### `-A` api [api ...] *[required]*

List of APIs to use during workload generation.\
If not passed, `-a` flag must be used instead.

## Args

No args are required.
